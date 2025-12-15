from alchemyBase import Base, FishingLine, FishingPole, FishingBait, FishingReel, PoleBait, Inventory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# Set up the database connection and session
engine = create_engine('sqlite:///fishing_inventory.db')
Session = sessionmaker(bind=engine)
session = Session(expire_on_commit=False)

# Inserting inventory items for various equipment
inventory_items = [
    Inventory(type='Fishing Line', item_id=1, quantity=10),
    Inventory(type='Fishing Line', item_id=2, quantity=5),
    Inventory(type='Fishing Reel', item_id=3, quantity=1),
    Inventory(type='Fishing Reel', item_id=4, quantity=4),
    Inventory(type='Fishing Poles', item_id=5, quantity=3),
    Inventory(type='Fishing Poles', item_id=6, quantity=2),
    Inventory(type='Fishing Bait', item_id=7, quantity=30),
    Inventory(type='Fishing Bait', item_id=8, quantity=10)
]
session.add_all(inventory_items)

fishing_lines = [
    FishingLine(line_id=1, line_material='Nylon', line_strength=50, line_length=100, item_id=1),
    FishingLine(line_id=2, line_material='Polyester', line_strength=40, line_length=120, item_id=2)
]
session.add_all(fishing_lines)

fishing_reels = [
    FishingReel(reel_id=1, reel_size='Medium', item_id=3),
    FishingReel(reel_id=2, reel_size='Large', item_id=4)
]
session.add_all(fishing_reels)

fishing_poles = [
    FishingPole(pole_id=1, pole_length=10, pole_material='Carbon Fiber', reel_id=1, line_id=1, item_id=5),
    FishingPole(pole_id=2, pole_length=12, pole_material='Fiberglass', reel_id=2, line_id=2, item_id=6)
]
session.add_all(fishing_poles)

fishing_baits = [
    FishingBait(bait_id=1, bait_type='Worm', bait_color='Red', item_id=7),
    FishingBait(bait_id=2, bait_type='Cricket', bait_color='Green', item_id=8)
]
session.add_all(fishing_baits)

pole_baits = [
    PoleBait(pole_id=1, bait_id=1),
    PoleBait(pole_id=2, bait_id=2)
]
session.add_all(pole_baits)

# Commit to the database
session.commit()