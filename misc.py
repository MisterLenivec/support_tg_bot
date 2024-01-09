from aiogram.fsm.storage.redis import Redis
from config_data.config import RedisSettings, load_config


redis_conf: RedisSettings = load_config().redis
redis = Redis(host=redis_conf.host)
