
# Import GeoLite2 Data into an SQL Database

MaxMind provides the
[GeoLite2](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data) free
geolocation data to provide location data from a IP address. Locations start as
country, but can be further narrowed to city.

They do provide an offline binary file that you can query locally, but I still
thought it would be fun to import the full CSV dump into a database, just for
experimental purposes.


## Supported Databases

I'm using the Python database ORM abstraction library
[SQLAlchemy](https://www.sqlalchemy.org/), so any database supported by that
will work. At the time of writing these include: SQLite, Postgresql,
MySQL & MariaDB, Oracle, and MS-SQL.


## Download Geolite2 CSV Data

You do have to sign up for a (free) account to download the CSV data needed
by this import script. It's provided as a pair of zip files. The small download
is for country-only data, and a large file for city-level data.
