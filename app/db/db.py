from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from app.config import MONGO_URL
import motor.motor_asyncio as asmotor



class DbData:
    client: AsyncIOMotorClient
    motor: AIOEngine
    fs = None


db = DbData()


async def start_db():
    global db
    db.client = AsyncIOMotorClient(MONGO_URL)
    db.motor = AIOEngine(motor_client=db.client, database="syskaoh")
    db.fs = asmotor.AsyncIOMotorGridFSBucket(db.client.images)
    print("db connexion established")


async def close_mongo_connection():
    db.client.close()
    print("db connexion closed")
