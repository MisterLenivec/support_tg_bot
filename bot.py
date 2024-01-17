import logging
from pathlib import Path

import ngrok
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from config_data.config import Config, load_config
from config_data.logging_settings import logging_config
from database.models import config_database
from handlers import fsm_handlers, user_handlers
from keyboards.main_menu import set_main_menu
from middlewares.throttling import ThrottlingMiddleware
from misc import redis
from services.db_service import add_default_answers_to_db


config: Config = load_config()

ROOT_PATH = Path.cwd()
PICTURES_PATH = ROOT_PATH.joinpath("media", "pictures")

# Webserver settings
# bind localhost only to prevent any external access
WEB_SERVER_HOST = config.webhook.web_server_host
# Port for incoming request from reverse proxy. Should be any available port
WEB_SERVER_PORT = config.webhook.web_server_port

# Path to webhook route, on which Telegram will send requests
WEBHOOK_PATH = config.webhook.webhook_path
# Secret key to validate requests from Telegram (optional)
WEBHOOK_SECRET = config.webhook.webhook_secret


async def on_startup(bot: Bot) -> None:
    logging.info('Database preparation.')
    await config_database()
    logging.info('The database has been configured.')

    logging.info('Checking default data in the DB.')
    await add_default_answers_to_db()

    logging.info('Connect to Ngrok.')
    listener = await ngrok.connect(f'{WEB_SERVER_HOST}:{WEB_SERVER_PORT}', authtoken_from_env=True)
    logging.info('Ngrok was connected.')

    # # Drop updates
    # await bot.delete_webhook(drop_pending_updates=True)

    logging.info('Installing a webhook.')
    await bot.set_webhook(f"{listener.url()}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)
    logging.info('Webhook has been installed.')

    # Setting up bot main menu
    await set_main_menu(bot)


def main():
    logging.info('Starting bot config.')
    storage = RedisStorage(redis=redis)
    logging.info('Redis storage was created.')

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)
    logging.info('Bot and Dispatcher were created.')

    # Register startup hook to initialize webhook
    dp.startup.register(on_startup)

    dp.include_router(user_handlers.router)
    dp.include_router(fsm_handlers.router)
    logging.info('Dispatcher was included handlers.')

    dp.message.middleware(ThrottlingMiddleware())
    logging.info('Dispatcher was included middlewares.')

    # Create aiohttp.web.Application instance
    app = web.Application()

    # Create an instance of request handler,
    # aiogram has few implementations for different cases of usage
    # In this example we use SimpleRequestHandler which is designed to handle simple cases
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    logging.info('Webhook requests handler was created.')

    # Register webhook handler on application
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    logging.info('Webhook requests handler was registered on app.')

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)
    logging.info('Mount dispatcher startup and shutdown hooks to aiohttp application.')

    # And finally start webserver
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    logging.info('Webserver is running.')


if __name__ == "__main__":
    # Logging config
    logging_config(ROOT_PATH, config.debug.debug_value)
    # Initializing logger
    logger = logging.getLogger(__name__)
    logger.info("Starting bot.")
    main()
