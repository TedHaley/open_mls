import enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Boolean, Column, Integer, String, Numeric, Enum, Date, Text
from database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    complete = Column(Boolean, default=False)


class PropertyType(enum.Enum):
    residential = 'residential'
    commercial = 'commercial'
    industrial = 'industrial'


class ResidentialBuildingType(enum.Enum):
    single_family = 'single family'
    multi_family = 'multi_family'
    condo = 'condo'


class CommercialBuildingType(enum.Enum):
    office = 'office'
    retail = 'retail'
    hotel = 'hotel'
    special_purpose = 'special purpose'


class IndustrialBuildingType(enum.Enum):
    manufacturing = 'manufacturing'
    warehouse = 'warehouse'
    flex_space = 'flex space'


class Title(enum.Enum):
    freehold = 'freehold'
    strata = 'strata'
    leasehold = 'leasehold'


class Listings(Base):
    __tablename__ = "listings"

    opem_mls_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = Column(String())
    longitude = Column(Numeric())
    latitude = Column(Numeric())
    price = Column(Integer())
    beds = Column(Numeric())
    baths = Column(Numeric())
    description = Column(Text())
    building_type = Column(Enum(ResidentialBuildingType))
    title = Column(Enum(Title))
    land_size_sqft = Column(Integer())
    floor_space_sqft = Column(Integer())
    built_in = Column(Integer())
    annual_property_taxes = Column(Integer())
    posted_on = Column(Date())
    active = Column(Boolean, default=True)
