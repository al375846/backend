
from app.config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient

from odmantic import AIOEngine


client = AsyncIOMotorClient(MONGO_URL)

db = AIOEngine(motor_client=client, database="syskaoh")