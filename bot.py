import logging
from pathlib import Path

import ngrok
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from config_data.config import Config, load_config
from database.models import config_database
from handlers import fsm_handlers, user_handlers
from keyboards.main_menu import set_main_menu
from misc import redis
from services.db_service import add_default_answers_to_db

# Initializing logger
logger = logging.getLogger(__name__)

config: Config = load_config()

PICTURES_PATH = Path.cwd().joinpath("media", "pictures")

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
    await config_database()
    await add_default_answers_to_db()

    listener = await ngrok.connect(f'{WEB_SERVER_HOST}:{WEB_SERVER_PORT}', authtoken_from_env=True)

    # # Drop updates
    # await bot.delete_webhook(drop_pending_updates=True)

    await bot.set_webhook(f"{listener.url()}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)
    # Setting up bot main menu
    await set_main_menu(bot)


def main():
    logger.info("Starting bot")

    storage = RedisStorage(redis=redis)

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    # Register startup hook to initialize webhook
    dp.startup.register(on_startup)

    dp.include_router(user_handlers.router)
    dp.include_router(fsm_handlers.router)

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

    # Register webhook handler on application
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

    # And finally start webserver
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    # Logging config
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )
    main()
