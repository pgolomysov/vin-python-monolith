import redis
from app.core.config import settings

redis_client = redis.from_url(settings.redis_url, decode_responses=True)

class RedisSyncClient():
    def get_messages_from_channel(self, channel_name: str, messages_count: int) -> list:
        return redis_client.rpop(channel_name, messages_count) or []

    def push_event_to_channel(self, channel_name: str, payload: {}) -> None:
        redis_client.lpush(channel_name, payload)
