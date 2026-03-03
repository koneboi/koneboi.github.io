import json

import pandas as pd
from django.db.models import Count, Q
from django.views.generic import DetailView, ListView, TemplateView

from .models import (
    AnalyticsDataset,
    Collaboration,
    LabExperience,
    NewsPost,
    Project,
    SavedFilter,
    Skill,
)


class HomePageView(TemplateView):
    template_name = "website/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_projects"] = Project.objects.all()[:3]
        context["latest_news"] = NewsPost.objects.published()[:3]
        return context


class ResearchPageView(TemplateView):
    template_name = "website/research.html"


class ProjectsPageView(TemplateView):
    template_name = "website/projects.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_type = self.request.GET.get("type")
        projects = Project.objects.all()
        if project_type and project_type != "all":
            projects = projects.filter(project_type=project_type)
        context["projects"] = projects
        context["project_types"] = Project.ProjectType.choices
        context["selected_type"] = project_type or "all"
        return context


class SkillsPageView(TemplateView):
    template_name = "website/skills.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skills = Skill.objects.all()
        context["skills"] = skills
        context["skill_chart_data"] = list(
            skills.values("name", "proficiency", "category")
        )
        return context


class LabsPageView(TemplateView):
    template_name = "website/labs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["labs"] = LabExperience.objects.all()
        collaborations = Collaboration.objects.select_related().prefetch_related(
            "projects", "labs"
        )
        context["collaborations"] = collaborations
        map_payload = []
        for item in collaborations:
            if item.latitude is None or item.longitude is None:
                continue
            map_payload.append(
                {
                    "name": item.name,
                    "summary": item.summary,
                    "region": item.region,
                    "lat": item.latitude,
                    "lng": item.longitude,
                    "duration": item.duration_label,
                }
            )
        context["collaborations_json"] = json.dumps(map_payload, default=str)
        return context


class AboutPageView(TemplateView):
    template_name = "website/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_count"] = Project.objects.count()
        context["lab_count"] = LabExperience.objects.count()
        return context


class ContactPageView(TemplateView):
    template_name = "website/contact.html"


class NewsPostListView(ListView):
    template_name = "website/news_list.html"
    model = NewsPost
    paginate_by = 12
    context_object_name = "news_items"

    def get_queryset(self):
        return NewsPost.objects.published()


class NewsPostPreviewView(DetailView):
    template_name = "website/news_preview.html"
    model = NewsPost
    context_object_name = "news"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return NewsPost.objects.all()


class AnalyticsPageView(TemplateView):
    template_name = "website/analytics.html"

    def get_publication_series(self):
        return []

    def get_project_series(self):
        return list(
            Project.objects.values("project_type")
            .annotate(total=Count("id"))
            .order_by("project_type")
        )

    def get_dataset_preview(self):
        dataset = AnalyticsDataset.objects.first()
        if not dataset:
            return None
        try:
            df = pd.read_csv(dataset.csv_file.path)
        except Exception as exc:
            return {"name": dataset.name, "error": str(exc)}
        preview = df.head(20)
        columns = list(preview.columns)
        rows = preview.to_dict(orient="records")
        table_rows = [[record.get(col, "") for col in columns] for record in rows]
        return {
            "id": dataset.id,
            "name": dataset.name,
            "columns": columns,
            "rows": table_rows,
            "description": dataset.description,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        publication_series = self.get_publication_series()
        project_series = self.get_project_series()
        dataset_preview = self.get_dataset_preview()
        context.update(
            {
                "publication_json": json.dumps(publication_series, default=str),
                "project_json": json.dumps(project_series, default=str),
                "dataset_preview": dataset_preview,
                "dataset_json": json.dumps(dataset_preview or {}, default=str),
            }
        )
        return context


class SearchResultsView(TemplateView):
    template_name = "website/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        filter_id = self.request.GET.get("filter")
        saved_filters = SavedFilter.objects.filter(is_public=True)
        selected_filter = None
        if filter_id:
            selected_filter = saved_filters.filter(pk=filter_id).first()

        project_results = Project.objects.all()

        if query:
            project_results = project_results.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(technologies__icontains=query)
            )

        if selected_filter:
            if selected_filter.filter_type == SavedFilter.FilterType.PROJECT:
                params = selected_filter.parameters or {}
                for key, value in params.items():
                    project_results = project_results.filter(**{key: value})
                if selected_filter.query:
                    project_results = project_results.filter(
                        Q(title__icontains=selected_filter.query)
                        | Q(description__icontains=selected_filter.query)
                    )

        context.update(
            {
                "query": query,
                "project_results": project_results[:25],
                "saved_filters": saved_filters,
                "selected_filter": selected_filter,
            }
        )
        return context
