from django.contrib import admin

from . import models


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "project_type", "published_on")
    list_filter = ("project_type",)
    search_fields = ("title", "description", "technologies")
    ordering = ("project_type", "title")


@admin.register(models.Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency")
    list_filter = ("category",)
    search_fields = ("name", "description")


@admin.register(models.LabExperience)
class LabExperienceAdmin(admin.ModelAdmin):
    list_display = ("lab_name", "role", "start_year", "end_year")
    list_filter = ("start_year", "end_year")
    search_fields = ("lab_name", "role", "focus")


@admin.register(models.NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ("title", "publish_at", "is_draft", "is_featured")
    list_filter = ("is_draft", "is_featured")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish_at"


@admin.register(models.ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "organization", "created_at")
    search_fields = ("name", "email", "organization", "message")
    readonly_fields = ("name", "email", "organization", "message", "created_at")


@admin.register(models.SavedFilter)
class SavedFilterAdmin(admin.ModelAdmin):
    list_display = ("name", "filter_type", "is_public", "created_at")
    list_filter = ("filter_type", "is_public")
    search_fields = ("name", "query")


@admin.register(models.AnalyticsDataset)
class AnalyticsDatasetAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "uploaded_by")
    search_fields = ("name", "description")
    readonly_fields = ("created_at",)


@admin.register(models.Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    list_display = ("name", "partner_type", "region", "start_year", "end_year")
    list_filter = ("partner_type", "region")
    search_fields = ("name", "summary", "grants", "responsibilities")
    filter_horizontal = ("labs", "projects")
