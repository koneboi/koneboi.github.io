from datetime import datetime
from email.utils import parsedate_to_datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from ingestion.services import RSSNewsFetcher
from website.models import NewsPost


def parse_timestamp(value: str) -> datetime:
    if not value:
        return timezone.now()
    try:
        dt = parsedate_to_datetime(value)
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.utc)
        return dt.astimezone(timezone.get_current_timezone())
    except (TypeError, ValueError):
        return timezone.now()


class Command(BaseCommand):
    help = "Sync news posts from an RSS feed into draft NewsPost entries."

    def add_arguments(self, parser):
        parser.add_argument("feed_url", help="RSS/Atom feed URL")
        parser.add_argument(
            "--limit", type=int, default=10, help="Number of entries to import"
        )
        parser.add_argument(
            "--publish",
            action="store_true",
            help="Mark imported entries as live immediately",
        )

    def handle(self, feed_url, *args, **options):
        fetcher = RSSNewsFetcher(feed_url)
        payloads = fetcher.fetch(limit=options["limit"])
        created = updated = 0
        for payload in payloads:
            publish_at = parse_timestamp(payload.published_at)
            defaults = {
                "title": payload.title[:255],
                "summary": payload.summary[:2000],
                "link": payload.link,
                "publish_at": publish_at,
                "is_draft": not options["publish"],
            }
            lookup = {"title": payload.title[:255]}
            if payload.link:
                lookup = {"link": payload.link}
            obj, created_flag = NewsPost.objects.update_or_create(
                defaults=defaults, **lookup
            )
            if created_flag:
                created += 1
            else:
                updated += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"News sync complete. {created} created, {updated} updated."
            )
        )
