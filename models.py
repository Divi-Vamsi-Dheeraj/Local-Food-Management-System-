# models.py
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Provider(Base):
    __tablename__ = "providers"
    Provider_ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Type = Column(String)
    Address = Column(String)
    City = Column(String)
    Contact = Column(String)
    food_listings = relationship("FoodListing", back_populates="provider")

class Receiver(Base):
    __tablename__ = "receivers"
    Receiver_ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Type = Column(String)
    City = Column(String)
    Contact = Column(String)
    claims = relationship("Claim", back_populates="receiver")

class FoodListing(Base):
    __tablename__ = "food_listings"
    Food_ID = Column(Integer, primary_key=True, index=True)
    Food_Name = Column(String)
    Quantity = Column(Integer)
    Expiry_Date = Column(Date)
    Provider_ID = Column(Integer, ForeignKey("providers.Provider_ID"))
    Provider_Type = Column(String)
    Location = Column(String)
    Food_Type = Column(String)
    Meal_Type = Column(String)
    provider = relationship("Provider", back_populates="food_listings")
    claims = relationship("Claim", back_populates="food_listing")

class Claim(Base):
    __tablename__ = "claims"
    Claim_ID = Column(Integer, primary_key=True, index=True)
    Food_ID = Column(Integer, ForeignKey("food_listings.Food_ID"))
    Receiver_ID = Column(Integer, ForeignKey("receivers.Receiver_ID"))
    Status = Column(String)
    Timestamp = Column(DateTime)
    food_listing = relationship("FoodListing", back_populates="claims")
    receiver = relationship("Receiver", back_populates="claims")
