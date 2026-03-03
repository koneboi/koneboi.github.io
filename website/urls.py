from django_distill import distill_path

from .views import (
    AboutPageView,
    AnalyticsPageView,
    ContactPageView,
    HomePageView,
    LabsPageView,
    NewsPostListView,
    ProjectsPageView,
    ResearchPageView,
    SearchResultsView,
    SkillsPageView,
)

urlpatterns = [
    distill_path("", HomePageView.as_view(), name="home", distill_func=lambda: [None]),
    distill_path(
        "research/",
        ResearchPageView.as_view(),
        name="research",
        distill_func=lambda: [None],
    ),
    distill_path(
        "projects/",
        ProjectsPageView.as_view(),
        name="projects",
        distill_func=lambda: [None],
    ),
    distill_path(
        "skills/", SkillsPageView.as_view(), name="skills", distill_func=lambda: [None]
    ),
    distill_path(
        "labs/", LabsPageView.as_view(), name="labs", distill_func=lambda: [None]
    ),
    distill_path(
        "about/", AboutPageView.as_view(), name="about", distill_func=lambda: [None]
    ),
    distill_path(
        "contact/",
        ContactPageView.as_view(),
        name="contact",
        distill_func=lambda: [None],
    ),
    distill_path(
        "analytics/",
        AnalyticsPageView.as_view(),
        name="analytics",
        distill_func=lambda: [None],
    ),
    distill_path(
        "news/", NewsPostListView.as_view(), name="news", distill_func=lambda: [None]
    ),
    distill_path(
        "search/",
        SearchResultsView.as_view(),
        name="search",
        distill_func=lambda: [None],
    ),
]
