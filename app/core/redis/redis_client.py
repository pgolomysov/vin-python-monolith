import redis as redis_sync
import redis.asyncio as redis_async
from app.core.config import settings

redis_sync_client = redis_sync.from_url(settings.redis_url, decode_responses=True)
redis_async_client = redis_async.from_url(settings.redis_url, decode_responses=True)

class RedisSyncClient():
    def get_messages_from_channel(self, channel_name: str, messages_count: int) -> list:
        return redis_sync_client.rpop(channel_name, messages_count) or []

    def push_event_to_channel(self, channel_name: str, payload: {}) -> None:
        redis_sync_client.lpush(channel_name, payload)

class RedisAsyncClient():
    async def get_messages_from_channel(self, channel_name: str, messages_count: int) -> list:
        return await redis_async_client.rpop(channel_name, messages_count) or []

    async def push_event_to_channel(self, channel_name: str, payload: {}) -> None:
        await redis_async_client.lpush(channel_name, payload)
