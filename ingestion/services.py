import logging
from dataclasses import dataclass
from typing import List, Optional

import feedparser
import requests

logger = logging.getLogger(__name__)


@dataclass
class PublicationPayload:
    title: str
    summary: str
    year: int
    topic: str
    doi_link: Optional[str] = None
    github_link: str = ""
    external_resource: str = ""


@dataclass
class NewsPayload:
    title: str
    summary: str
    link: str
    published_at: str


class CrossrefPublicationFetcher:
    """Fetch publications using the Crossref API as a stand-in for Scholar/ORCID."""

    API_URL = "https://api.crossref.org/works"

    def __init__(self, query: str = "genomics", rows: int = 20):
        self.query = query
        self.rows = rows

    def fetch(self) -> List[PublicationPayload]:
        params = {
            "query": self.query,
            "rows": self.rows,
            "sort": "published",
            "order": "desc",
        }
        try:
            response = requests.get(self.API_URL, params=params, timeout=15)
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.error("Crossref fetch failed: %s", exc)
            return []

        data = response.json().get("message", {}).get("items", [])
        payloads: List[PublicationPayload] = []
        for item in data:
            title = " ".join(item.get("title", [])).strip() or "Untitled"
            abstract = (item.get("abstract") or "").strip()
            doi = item.get("DOI")
            year = (
                item.get("published-print", {}).get("date-parts", [[None]])[0][0]
                or item.get("issued", {}).get("date-parts", [[None]])[0][0]
                or 0
            )
            topic = (item.get("container-title") or ["Genomics"])[0]
            payloads.append(
                PublicationPayload(
                    title=title,
                    summary=abstract or "Automatically imported from Crossref.",
                    year=int(year or 0),
                    topic=topic,
                    doi_link=f"https://doi.org/{doi}" if doi else "",
                    external_resource=item.get("URL", ""),
                )
            )
        return payloads


class RSSNewsFetcher:
    """Fetch news items from an RSS feed (placeholder for Google Scholar / lab blogs)."""

    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    def fetch(self, limit: int = 10) -> List[NewsPayload]:
        try:
            feed = feedparser.parse(self.feed_url)
        except Exception as exc:  # pragma: no cover - feedparser already robust
            logger.error("RSS parsing failed: %s", exc)
            return []

        entries = feed.get("entries", [])[:limit]
        payloads: List[NewsPayload] = []
        for entry in entries:
            payloads.append(
                NewsPayload(
                    title=entry.get("title", "Untitled"),
                    summary=entry.get("summary", ""),
                    link=entry.get("link", ""),
                    published_at=entry.get("published", entry.get("updated", "")),
                )
            )
        return payloads
