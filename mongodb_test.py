#!/usr/bin/env python3
"""
Test MongoDB connectivity
"""

from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent / "backend"
load_dotenv(ROOT_DIR / '.env')

async def test_mongodb():
    """Test MongoDB connectivity"""
    try:
        print("Testing MongoDB connectivity...")
        print(f"URL: {os.environ['MONGO_URL']}")
        print(f"Database: {os.environ['DB_NAME']}")
        
        client = AsyncIOMotorClient(os.environ['MONGO_URL'])
        db = client[os.environ['DB_NAME']]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful")
        
        # Test database operations
        test_collection = db.test_collection
        
        # Insert test document
        result = await test_collection.insert_one({"test": "data", "timestamp": "2025-01-01"})
        print(f"✅ Insert successful: {result.inserted_id}")
        
        # Find test document
        doc = await test_collection.find_one({"_id": result.inserted_id})
        print(f"✅ Find successful: {doc}")
        
        # Delete test document
        await test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Delete successful")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("MONGODB CONNECTIVITY TEST")
    print("=" * 60)
    
    asyncio.run(test_mongodb())