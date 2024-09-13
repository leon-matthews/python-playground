
from collections import namedtuple
from ipaddress import IPv4Address
import logging

from sqlalchemy import Column, create_engine, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()

logger = logging.getLogger(__name__)

GeoIP2 = namedtuple('GeoIP2', 'city country iso3166 latitude longitude time_zone')


def connect():
    """
    Create an SQLAlchemy session instance.
    """
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def find(session, ip):
    """
    Attempt to find data for given IP address.

    Args:
        session:
            SQLAlchemy session.
        ip:
            Anything that an IPv4Address constructor will accept.

    Returns (GeoIP2|None)
        A GeoIP2 namedtuple if found, otherwise None.
    """
    # Query database
    ip = int(IPv4Address(ip))
    query = session.query(BlockIP4, City, Country)
    query = query.filter(ip >= BlockIP4.first, ip <= BlockIP4.last)
    query = query.outerjoin(City, BlockIP4.city_id==City.id)
    query = query.outerjoin(Country, City.country_id==Country.id)

    # Check results
    found = query.all()

    if not found:
        return None

    if (num_found := len(found)) > 1:
        logger.warning(
            "Found %s IPv4 blocks that match %s, using the first.",
            num_found, IPv4Address(ip)
        )

    # Assemble record to return
    block, city, country = found[0]
    geoip2 = GeoIP2(
        city=city.name,
        country=country.name,
        iso3166=country.iso3166,
        latitude=city.latitude,
        longitude=city.longitude,
        time_zone=city.time_zone,
    )
    return geoip2


class BlockIP4(Base):
    __tablename__ = 'block_ip4'

    # Fields
    id = Column(Integer, primary_key=True)
    first = Column(Integer, nullable=False)
    last = Column(Integer, nullable=False)

    # Relationships
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship('City')
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship('Country')

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}(id={self.id}, "
            f"first={IPv4Address(self.first)}, last={IPv4Address(self.last)})>"
        )

    def __str__(self):
        return f"{IPv4Address(self.first)} to {IPv4Address(self.last)}"


class City(Base):
    __tablename__ = 'city'

    # Fields
    id = Column(Integer, primary_key=True)
    name = Column(String(127), nullable=False)
    time_zone = Column(String(31))
    latitude = Column(Float)
    longitude = Column(Float)

    # Relationships
    country_id = Column(Integer, ForeignKey('country.id'), nullable=False)
    country = relationship(
        'Country',
        back_populates='cities',
        foreign_keys=(country_id,),
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name={self.name})>"

    def __str__(self):
        return self.name


class Country(Base):
    __tablename__ = 'country'

    # Fields
    id = Column(Integer, primary_key=True)
    name = Column(String(127), nullable=False)
    iso3166 = Column(String(2))

    # Relationships
    cities = relationship(
        'City',
        back_populates='country',
        foreign_keys=(City.country_id,),
        order_by=City.name)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name={self.name})>"

    def __str__(self):
        return self.name
