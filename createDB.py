from sqlalchemy import create_engine

# Import models from the hw7base file
from alchemyBase import Base, FishingLine, FishingPole, FishingBait, FishingReel, PoleBait, Inventory

# To show the SQL that is running
import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Create database engine
engine = create_engine('sqlite:///fishing_inventory.db')

# This will create all tables based on the models
Base.metadata.create_all(engine)