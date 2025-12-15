from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create a base class for declarative class definitions
Base = declarative_base()

# Inventory table
class Inventory(Base):
    __tablename__ = 'Inventory'
    type = Column(String, primary_key=True)
    item_id = Column(Integer, primary_key=True)
    quantity = Column(Integer)

    # Relationships (referencing class names, not tables)
    fishing_lines = relationship("FishingLine", back_populates="inventory", uselist=False)
    fishing_reels = relationship("FishingReel", back_populates="inventory", uselist=False)
    fishing_poles = relationship("FishingPole", back_populates="inventory", uselist=False)
    fishing_baits = relationship("FishingBait", back_populates="inventory", uselist=False)

# FishingLine table
class FishingLine(Base):
    __tablename__ = 'FishingLine'
    line_id = Column(Integer, primary_key=True)
    line_material = Column(String)
    line_strength = Column(Integer)
    line_length = Column(Integer)
    item_id = Column(Integer, ForeignKey('Inventory.item_id'))

    # Relationships (back reference to the Inventory table)
    inventory = relationship("Inventory", back_populates="fishing_lines")

    def __repr__(self):
        return f"FishingLine(line_id='{self.line_id}', line_material='{self.line_material}', line_strength='{self.line_strength}', line_length='{self.line_length}', item_id='{self.item_id}')"

# FishingReel table
class FishingReel(Base):
    __tablename__ = 'FishingReel'
    reel_id = Column(Integer, primary_key=True)
    reel_size = Column(String)
    item_id = Column(Integer, ForeignKey('Inventory.item_id'))

    # Relationships (back reference to the Inventory table)
    inventory = relationship("Inventory", back_populates="fishing_reels")

    def __repr__(self):
        return f"FishingReel(reel_id='{self.reel_id}', reel_size='{self.reel_size}', item_id='{self.item_id}')"

# FishingPole table
class FishingPole(Base):
    __tablename__ = 'FishingPole'
    pole_id = Column(Integer, primary_key=True)
    pole_length = Column(Integer)
    pole_material = Column(String)
    reel_id = Column(Integer, ForeignKey('FishingReel.reel_id'))
    line_id = Column(Integer, ForeignKey('FishingLine.line_id'))
    item_id = Column(Integer, ForeignKey('Inventory.item_id'))

    # Relationships (back references)
    inventory = relationship("Inventory", back_populates="fishing_poles")
    fishing_reel = relationship("FishingReel")
    fishing_line = relationship("FishingLine")

    def __repr__(self):
        return f"FishingPole(pole_id='{self.pole_id}', pole_length='{self.pole_length}', pole_material='{self.pole_material}', reel_id='{self.reel_id}', line_id='{self.line_id}', item_id='{self.item_id}')"

# FishingBait table
class FishingBait(Base):
    __tablename__ = 'FishingBait'
    bait_id = Column(Integer, primary_key=True)
    bait_type = Column(String)
    bait_color = Column(String)
    item_id = Column(Integer, ForeignKey('Inventory.item_id'))

    # Relationships (back reference to the Inventory table)
    inventory = relationship("Inventory", back_populates="fishing_baits")

    #printable representation
    def __repr__(self):
        return f"FishingBait(bait_id='{self.bait_id}', bait_type='{self.bait_type}', bait_color='{self.bait_color}', item_id='{self.item_id}')"

# PoleBait table
class PoleBait(Base):
    __tablename__ = 'PoleBait'
    pole_id = Column(Integer, ForeignKey('FishingPole.pole_id'), primary_key=True)
    bait_id = Column(Integer, ForeignKey('FishingBait.bait_id'), primary_key=True)

    # Relationships
    fishing_pole = relationship("FishingPole")
    fishing_bait = relationship("FishingBait")

    def __repr__(self):
        return f"PoleBait(pole_id='{self.pole_id}', bait_id='{self.bait_id}')"