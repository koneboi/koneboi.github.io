import factory
from django.utils import timezone

from website import models


class PublicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Publication

    title = factory.Sequence(lambda n: f"Genome Insight {n}")
    journal = "Genome Research"
    year = 2024
    topic = "Genomics"
    summary = "Demonstration publication."
    doi_link = factory.LazyAttribute(
        lambda o: f"https://doi.org/10.1000/{o.title.replace(' ', '').lower()}"
    )
    github_link = "https://github.com/example/project"
    external_resource = "https://scholar.google.com"
    featured = False


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Project

    title = factory.Sequence(lambda n: f"Pipeline {n}")
    description = "End-to-end bioinformatics pipeline."
    technologies = "Nextflow, Docker"
    project_type = models.Project.ProjectType.GENOMICS_PIPELINE
    duration = "2024"
    link = "https://example.org/project"
    repository = "https://github.com/example/pipeline"
    published_on = factory.LazyFunction(lambda: timezone.now().date())


class NewsPostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.NewsPost

    title = factory.Sequence(lambda n: f"News {n}")
    summary = "A sample news update."
    link = "https://example.org/news"
    publish_at = factory.LazyFunction(
        lambda: timezone.now() - timezone.timedelta(days=1)
    )
    is_draft = False
    is_featured = False
