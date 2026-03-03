import pytest
from django.urls import reverse
from django.utils import timezone

from tests.factories import NewsPostFactory, ProjectFactory, PublicationFactory
from website.models import NewsPost


@pytest.mark.django_db
def test_newspost_manager_returns_only_live_posts():
    live = NewsPostFactory()
    NewsPostFactory(is_draft=True)
    NewsPostFactory(publish_at=timezone.now() + timezone.timedelta(days=2))

    qs = NewsPost.objects.published()
    assert list(qs) == [live]


@pytest.mark.django_db
def test_search_view_returns_publications_and_projects(client):
    PublicationFactory(title="RNA-Seq Benchmark")
    ProjectFactory(title="RNA Pipeline", description="RNA-Seq reference implementation")

    response = client.get(reverse("search"), {"q": "RNA"})
    assert response.status_code == 200
    body = response.content.decode()
    assert "RNA-Seq Benchmark" in body
    assert "RNA Pipeline" in body


@pytest.mark.django_db
def test_contact_page_loads(client):
    response = client.get(reverse("contact"))
    assert response.status_code == 200
    body = response.content.decode()
    assert "mailto:" in body


@pytest.mark.django_db
def test_analytics_page_loads(client):
    PublicationFactory(year=2023)
    PublicationFactory(year=2024)

    response = client.get(reverse("analytics"))
    assert response.status_code == 200
    body = response.content.decode()
    assert "Publications by Year" in body
