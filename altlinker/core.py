import logging
import re
from typing import Tuple
from urllib.parse import urlparse

import httpx

from altlinker import config

logger = logging.getLogger(__name__)


def get_urls_in_text(text: str, services: list[str]) -> set[str]:
    """find all urls that have alternative frontends in a message"""
    domains = "|".join(re.escape(domain) for domain in services)
    regex = (
        rf"(?:(?:https?:)?//)?(?:www\.)?(?:{domains})[\w\-\./\?\#\%\&\=\+]+"
    )
    return set(re.findall(regex, text))


def clean_url(url: str) -> str:
    return re.sub(r"^https?:\/\/(www.)?", "", url)


async def get_url_from_farside(url: str) -> str:
    """get altenative url of a given url from farside service"""
    farside_url = "https://farside.link/" + clean_url(url)
    agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0"
    headers = {"User-Agent": agent}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.head(
                farside_url, headers=headers, follow_redirects=True, timeout=3
            )
            return str(response.url)
        except httpx.RequestError as e:
            logger.info("error", e)
        except Exception as e:
            logger.info("error", e)
        return farside_url


def get_fallback_alt_url(url: str) -> str:
    """generate an alternative url from fallback service instances"""
    parsed_url = urlparse(url)
    domain_name = parsed_url.hostname.replace("www.", "")
    fallback = config.FALLBACK_INSTANCES.get(domain_name)
    if not fallback:
        return url
    return url.replace(domain_name, fallback)


async def get_alt_url(url: str) -> str:
    """find alternative url from different sources with fallbacks"""
    alt_url = await get_url_from_farside(url)
    return alt_url or get_fallback_alt_url(url)


def has_alt_urls(text: str) -> bool:
    """check if text has services with alt urls"""
    return len(get_urls_in_text(text, config.SERVICES)) > 0


async def get_alt_urls_in_text(text: str) -> list[Tuple[str, str]]:
    """find all urls in text and get alternatives of them"""
    urls = get_urls_in_text(text, config.SERVICES)
    alt_url_pairs: list[Tuple[str, str]] = []
    for url in urls:
        alt_url_pairs.append((url, await get_alt_url(url)))
    return alt_url_pairs


async def replace_alternate_url_in_text(text: str) -> str | None:
    """modify the message to append or replace alternative urls"""
    alt_url_pairs = await get_alt_urls_in_text(text)
    if not alt_url_pairs:
        return None
    for url, alt_url in alt_url_pairs:
        text = text.replace(url, alt_url)
    return text
