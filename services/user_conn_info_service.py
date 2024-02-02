from dataclasses import dataclass
from redis.asyncio import Redis

@dataclass
class UserConnectionInfo:
    api_id: int
    api_hash: str
    phone_number: str


class UserConnInfoService:
    def __init__(self, redis_client: Redis) -> None:
        self.client = redis_client

    async def save_user_conn_info(self, user_id: int, user_conn_info: UserConnectionInfo) -> None:
        '''
        saves the user connection info to the redis server. If already existing, they are replaced
        '''
        await self.client.hset(f'userConnInfo:{user_id}', mapping = {
            'apiId': user_conn_info.api_id,
            'apiHash': user_conn_info.api_hash,
            'phoneNumber': user_conn_info.phone_number
        })

    async def get_user_conn_info(self, user_id: int) -> UserConnectionInfo:
        '''
        get the user connection info for `user_id` from the redis server
        '''
        user_conn_info_map = await self.client.hgetall(f'userConnInfo:{user_id}')
        return UserConnectionInfo(**user_conn_info_map)