from django.core.management.base import BaseCommand

from ingestion.services import CrossrefPublicationFetcher
from website.models import Publication


class Command(BaseCommand):
    help = "Sync publications from Crossref or a similar scholarly API."

    def add_arguments(self, parser):
        parser.add_argument("--query", default="genomics", help="Search term")
        parser.add_argument(
            "--rows", type=int, default=20, help="Number of records to fetch"
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Fetch data without writing to the database",
        )

    def handle(self, *args, **options):
        fetcher = CrossrefPublicationFetcher(
            query=options["query"],
            rows=options["rows"],
        )
        payloads = fetcher.fetch()
        created = updated = 0
        for payload in payloads:
            defaults = {
                "title": payload.title,
                "year": payload.year or 0,
                "summary": payload.summary[:2000],
                "topic": payload.topic or "Genomics",
                "github_link": payload.github_link,
                "external_resource": payload.external_resource,
                "featured": False,
            }
            if payload.doi_link:
                lookup = {"doi_link": payload.doi_link}
            else:
                lookup = {"title": payload.title, "year": defaults["year"]}
            if options["dry_run"]:
                self.stdout.write(f"[dry-run] Would upsert: {payload.title}")
                continue
            obj, created_flag = Publication.objects.update_or_create(
                **lookup,
                defaults=defaults,
            )
            if created_flag:
                created += 1
            else:
                updated += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Sync complete. {created} created, {updated} updated (query='{options['query']}')."
            )
        )
