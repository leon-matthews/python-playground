#!/usr/bin/env python3

from collections import namedtuple
from dataclasses import asdict, dataclass
import datetime
import json
import logging
from pprint import pprint as pp
import re
import sys
import time
from urllib.parse import urlencode, urljoin, urlsplit, urlunsplit
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup, SoupStrainer, Tag
from rich import inspect, print as rprint
import requests_cache


logger = logging.getLogger(__name__)


BASE_URL = 'https://www.raredisorders.org.nz/'
Category = namedtuple('Category', 'name url excerpt')
THROTTLE_DELAY = 1.0
TZ = ZoneInfo("Pacific/Auckland")

CATEGORIES = (
    Category(
        'News',
        '/about-us/news/',
        'The latest updates from RDNZ and the rare disorder community.',
    ),
    Category(
        'Newsletters',
        '/about-us/newsletters-2/',
        'Bi-monthly news and views from the connector hub and collective '
        'voice of rare disorders in New Zealand.',
    ),
    Category(
        'Stories',
        '/about-rare-disorders/stories-project/',
        'Meet some of the 300,000 people living with a rare disorder in New Zealand.',
    ),
    Category(
        'Submissions',
        '/about-us/submissions/',
        'RDNZ actively engages with rare disease issues by responding to '
        'calls for submissions.',
    ),
)


@dataclass
class BlogEntry:
    """
    Historical blog entry.
    """
    title: str
    excerpt: str
    date: datetime.datetime
    url: str                            # URL path to detail page
    body: str = ''                      # HTML
    category: str = ''
    image: str = ''                     # URL path to cover image


def clean_text(string: str) -> str:
    """
    Clean given string, removing repeated spaces, newlines, and 'smart' quotes.
    """
    string = re.sub(r'\s+', ' ', string)
    string = plain_quotes(string)
    string = string.strip()
    return string


def download(session, url: str) -> str:
    """
    Fetch HTML from given URL.

    Returns:
        Full unicode HTML string.
    """
    response = session.get(url)
    response.raise_for_status()

    # Be friendly and slow down for requests against remote server
    if not response.from_cache:
        logger.info(f"Downloaded {url}")
        time.sleep(THROTTLE_DELAY)

    html = response.text
    html = html.replace('\r\n', '\n')
    return html


def join_url(base: str, path: str) -> str:
    """
    Join a domain and path parts of a URL together.

    Similar to `urllib.parse.urljoin()`, but adds in a default schema
    if one not provided.

    Args:
        base:
            Base URL. May contain a schema and an existing path.
        path:
            File name or full path.

    Returns:
        Full URL.
    """
    if '//' not in base:
        base = 'http://' + base
    return urljoin(base, path)


def make_blog_entry(card: Tag) -> BlogEntry:
    """
    Make `BlogEntry` from the card div from the news list page.

    Args:
        card:
            The HTML div containing the blog entry.

    Returns:
        A (partially) populated BlogEntry object.
    """
    title = card.find('a', class_="stretched-link").string
    title = clean_text(title)
    excerpt = card.find('p', class_="card-text").string
    excerpt = clean_text(excerpt)
    date = parse_datetime(card.find('div', class_='card-body').small.span.string)
    url = card.find('a', class_='stretched-link').attrs['href']

    return BlogEntry(
        title=title,
        excerpt=excerpt,
        date=date.isoformat(),
        url=url,
    )


def make_json(entries: list[BlogEntry]) -> str:
    """
    Create JSON string from blog entry data.
    """
    data = []
    for entry in entries:
        data.append(asdict(entry))
    return json.dumps(data, indent=4)


def parse_datetime(string: str) -> datetime.datetime:
    """
    Parse date and time from scraped data.

    Args:
        string:
            Time string from old website, in format: "Aug 7, 2018, 11:42 AM"

    Returns:
        Timezone-aware (NZST) datetime object.
    """
    # Aug 7, 2018, 11:42 AM
    format_ = "%b %d, %Y, %I:%M %p"
    naive = datetime.datetime.strptime(string, format_)
    aware = naive.astimezone(TZ)
    return aware


def parse_detail(html: str, entry: BlogEntry) -> None:
    """
    Add field to the given blog entry from blog detail HTML.
    """
    soup = BeautifulSoup(html, 'html.parser')
    section = soup.find('section', class_="content")

    # Cover image
    try:
        entry.image = section.find('img').attrs['src']
    except AttributeError:
        entry.image = ''

    # Body text
    strings = []
    for p in section.find_all('p'):
        # Skip certain paragraphs
        if 'class' in p.attrs:
            class_string = p.attrs['class']
            if 'd-print-none' in class_string:
                continue
        strings.append(p.string)

    paragraphs = [f"<p>\n{s}\n</p>" for s in strings]
    entry.body = '\n\n'.join(paragraphs)


def parse_list(html: str) -> list[BlogEntry]:
    """
    Create (partial) BlogEntry objects from blog entry list.

    All of the BlogEntry fields are filled in except for the body. We need
    to dowload the detail page to do that.

    Args:
        Raw HTML text for a blog list.

    Returns:
        A list of the blog entries found in HTML.
    """
    soup = BeautifulSoup(html, 'html.parser')
    entries = []

    # Parent div
    container = soup.find('div', class_="grid-layout my-4")
    cards = container.find_all('div', class_='card mb-3')
    for card in cards:
        entry = make_blog_entry(card)
        entries.append(entry)
    return entries


def plain_quotes(string: str) -> str:
    """
    Replace 'smart' or 'curly' quotes with their 'normal' equivilants.

    >>> plain_quotes('“...”')
    '"..."'

    Returns:
        Plain-ascii double or single quotes.
    """
    single = u"'"
    double = u'"'
    mapping = {
        34: single,     # " \u0022 QUOTATION MARK
        39: single,     # ' \u0027 APOSTROPHE
        171: double,    # « \u00ab LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
        187: double,    # » \u00bb RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
        1370: single,   # ՚ \u055a ARMENIAN APOSTROPHE
        8216: single,   # ‘ \u2018 LEFT SINGLE QUOTATION MARK
        8217: single,   # ’ \u2019 RIGHT SINGLE QUOTATION MARK
        8218: single,   # ‚ \u201a SINGLE LOW-9 QUOTATION MARK
        8219: single,   # ‛ \u201b SINGLE HIGH-REVERSED-9 QUOTATION MARK
        8220: double,   # “ \u201c LEFT DOUBLE QUOTATION MARK
        8221: double,   # ” \u201d RIGHT DOUBLE QUOTATION MARK
        8222: double,   # „ \u201e DOUBLE LOW-9 QUOTATION MARK
        8223: double,   # ‟ \u201f DOUBLE HIGH-REVERSED-9 QUOTATION MARK
        8249: single,   # ‹ \u2039 SINGLE LEFT-POINTING ANGLE QUOTATION MARK
        8250: single,   # › \u203a SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
        12317: double,  # 〝 \u301d REVERSED DOUBLE PRIME QUOTATION MARK
        12318: double,  # 〞 \u301e DOUBLE PRIME QUOTATION MARK
        12319: double,  # 〟 \u301f LOW DOUBLE PRIME QUOTATION MARK
        65282: single,  # ＂\uff02 FULLWIDTH QUOTATION MARK
        65287: single,  # ＇\uff07 FULLWIDTH APOSTROPHE
    }
    return string.translate(mapping)


def scrape_detail(session, url: str, entry: BlogEntry) -> None:
    """
    Fill in given BlogEntry object from its HTML detail page.
    """
    html = download(session, url)
    body = parse_detail(html, entry)


def scrape_index(session, url: str, category: str) -> list[BlogEntry]:
    """
    Download all of the index pages for the given category.

    Args:
        session:
            Request session
        url:
            Full URL to index page, excluding page query
        category:
            Name of category, eg. 'News'

    Returns:
        List of partially-filled in BlogEntry objects.
    """
    # Parse index pages and paginate
    entries = []
    limit = 1000
    stride = 10
    for start in range(0, limit, stride):
        page_url = f"{url}?start={start}"
        html = download(session, page_url)
        page_entries = parse_list(html)
        if len(page_entries) == 0:
            break
        entries.extend(page_entries)

    # Fill in category
    for entry in entries:
        entry.category = category

    return entries


def main() -> int:
    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
    )
    session = requests_cache.CachedSession('cache')

    # Scrape index pages
    entries = []
    for category in CATEGORIES:
        url = join_url(BASE_URL, category.url)
        entries.extend(scrape_index(session, url, category.name))
    logger.info("Scraped %s blog entries from index pages", len(entries))

    # Fill-in BlogEntry objects by scraping detail URLs
    for count, entry in enumerate(entries, 1):
        url = join_url(BASE_URL, entry.url)
        scrape_detail(session, url, entry)
    logger.info("Scraped %s blog detail pages", count)

    # Export to JSON
    print(make_json(entries))

    return 0


if __name__ == '__main__':
    sys.exit(main())
