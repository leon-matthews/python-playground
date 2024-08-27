
from ipaddress import IPv4Network
from pprint import pprint as pp
from unittest import TestCase

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from geolite2.db import Base, BlockIP4, City, Country, connect
from geolite2.utils import calculate_range


def add_block_ipv4(session, network, country=None, city=None):
    """
    Add an IPv4 network block to the database session.

    Args:
        session:
            An SQLAlchemy session.
        city:
            An existing `City` object.
        network:
            Either an `IPv4Network` object, or anything that its constructor
            accepts, eg. '192.168.0.0/24'.

    Returns: BlockIP4
        Returns the block that was just added to the DB session.
    """
    network = IPv4Network(network)
    first, last = calculate_range(network)
    block = BlockIP4(
        first=first,
        last=last,
        city=city,
    )
    session.add(block)
    return block


def create_block_ipv4(network, country=None, city=None):
    """
    Build a IPv4 network block object.

    Args:
        network (IPv4Network):
            Either an `IPv4Network` object, or anything that its constructor
            accepts, eg. '192.168.0.0/24'.
        country (Country):
            Optional existing `Country` object.
        city (City):
            Optional existing `City` object.

    Returns: BlockIP4
    """
    network = IPv4Network(network)
    first, last = calculate_range(network)
    block = BlockIP4(
        first=first,
        last=last,
        country=country,
        city=city,
    )
    return block


def add_city(session, country, **kwargs):
    """
    Add a city object to the given session.

    Args:
        session:
            An SQLAlchemy session.
    """
    fields = {
        'name': 'Auckland',
        'time_zone': 'Pacific/Auckland',
        'latitude': -36.8483,
        'longitude': 174.7625,
        'country': country,
    }
    fields.update(kwargs)
    city = City(**fields)
    session.add(city)
    return city


def add_country(session, **kwargs):
    fields = {
        'name': 'New Zealand',
        'iso3166': 'NZ',
    }
    fields.update(kwargs)
    country = Country(**fields)
    session.add(country)
    return country


AUCKLAND = {
    'name': 'Auckland',
    'time_zone': 'Pacific/Auckland',
    'latitude': -36.8483,
    'longitude': 174.7625,
}


WELLINGTON = {
    'name': 'Wellington',
    'time_zone': 'Pacific/Auckland',
    'latitude': -41.288889,
    'longitude': 174.777222,
}


class TransactionTestCase(TestCase):
    """
    Efficient test isolation for unit tests using SQLAlchemy's ORM interface.

    Each test method is wrapped in its own transaction - writes to the database
    in any one function do not affect any other function.

    For efficiency's sake, the database connection and its tables are
    created only one per test class.
    """

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')

        # Enable 'nested' transactions (SAVEPOINT) for SQLite.
        # This is a work-around for long-standing Python SQLite3 bugs. See:
        # https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#pysqlite-serializable
        @event.listens_for(cls.engine, "connect")
        def do_connect(dbapi_connection, connection_record):
            dbapi_connection.isolation_level = None

        @event.listens_for(cls.engine, "begin")
        def do_begin(conn):
            conn.execute("BEGIN")

        Base.metadata.create_all(cls.engine)
        Session = sessionmaker(bind=cls.engine, autocommit=False)
        cls.session = Session()

    def setUp(self):
        self.session.begin_nested()

    def tearDown(self):
        self.session.rollback()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        Base.metadata.drop_all(cls.engine)


class DataTestCase(TestCase):
    """
    Test case base class with a small set of test data thrown in.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.session = connect()

        cls.nz = add_country(cls.session)
        cls.auckland = add_city(cls.session, cls.nz, **AUCKLAND)
        cls.wellington = add_city(cls.session, cls.nz, **WELLINGTON)

        # Create IPv4 Blocks
        cls.block = add_block_ipv4(cls.session, '192.168.1.0/24', None, cls.wellington)
        cls.block = add_block_ipv4(cls.session, '192.168.2.0/24', None, cls.auckland)
        cls.block = add_block_ipv4(cls.session, '192.168.3.0/24', None, cls.wellington)
        cls.session.commit()
