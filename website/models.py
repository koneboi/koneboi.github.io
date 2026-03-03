from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify


class Publication(models.Model):
    """Scientific publications and research outputs."""

    title = models.CharField(max_length=255)
    journal = models.CharField(max_length=255, blank=True)
    year = models.PositiveSmallIntegerField()
    topic = models.CharField(max_length=120)
    summary = models.TextField()
    doi_link = models.URLField(blank=True)
    github_link = models.URLField(blank=True)
    external_resource = models.URLField(
        blank=True, help_text="Link to Google Scholar or similar"
    )
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-year", "-id"]

    def __str__(self) -> str:
        return f"{self.title} ({self.year})"


class Project(models.Model):
    """Computational or wet-lab project descriptions."""

    class ProjectType(models.TextChoices):
        GENOMICS_PIPELINE = "genomics", "Genomics Pipeline"
        BIOINFORMATICS_TOOL = "bioinformatics", "Bioinformatics Tool"
        MODELING = "modeling", "Modeling & Simulation"
        DATA_RESOURCE = "data", "Data Resource"

    title = models.CharField(max_length=255)
    description = models.TextField()
    technologies = models.CharField(max_length=255, help_text="Comma-separated list")
    project_type = models.CharField(
        max_length=20,
        choices=ProjectType.choices,
        default=ProjectType.GENOMICS_PIPELINE,
    )
    duration = models.CharField(max_length=100, blank=True)
    link = models.URLField(blank=True)
    repository = models.URLField(blank=True)
    published_on = models.DateField(default=timezone.now)

    class Meta:
        ordering = ["project_type", "title"]

    def __str__(self) -> str:
        return self.title


class Skill(models.Model):
    """Skill proficiency visualizations."""

    CATEGORY_CHOICES = [
        ("programming", "Programming"),
        ("bioinformatics", "Bioinformatics Platforms"),
        ("statistics", "Statistics & Modeling"),
        ("cloud", "Cloud & DevOps"),
    ]

    name = models.CharField(max_length=120)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    proficiency = models.PositiveSmallIntegerField(help_text="Percentage 0-100")
    description = models.CharField(max_length=255, blank=True)
    example_link = models.URLField(blank=True)

    class Meta:
        ordering = ["category", "-proficiency"]

    def __str__(self) -> str:
        return f"{self.name} ({self.proficiency}%)"


class LabExperience(models.Model):
    """Timeline of laboratory and research experience."""

    lab_name = models.CharField(max_length=255)
    role = models.CharField(max_length=120)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(blank=True, null=True)
    location = models.CharField(max_length=120, blank=True)
    focus = models.CharField(
        max_length=255, help_text="Key techniques or research focus"
    )
    description = models.TextField()
    report_link = models.URLField(blank=True)

    class Meta:
        ordering = ["-start_year"]

    def __str__(self) -> str:
        return f"{self.lab_name} - {self.role}"

    @property
    def duration_label(self) -> str:
        end = self.end_year or "Present"
        return f"{self.start_year} – {end}"


class NewsPostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            is_draft=False,
            publish_at__lte=now,
        ).filter(Q(unpublish_at__isnull=True) | Q(unpublish_at__gt=now))


class NewsPost(models.Model):
    """News and announcements editable via the dashboard."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    summary = models.TextField()
    link = models.URLField(blank=True)
    publish_at = models.DateTimeField(default=timezone.now)
    unpublish_at = models.DateTimeField(blank=True, null=True)
    is_draft = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = NewsPostQuerySet.as_manager()

    class Meta:
        ordering = ["-publish_at", "-id"]

    def __str__(self) -> str:
        return f"{self.title} ({self.publish_at:%Y-%m-%d})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or f"news-{timezone.now():%Y%m%d%H%M%S}"
            slug_candidate = base_slug
            index = 1
            while (
                NewsPost.objects.filter(slug=slug_candidate)
                .exclude(pk=self.pk)
                .exists()
            ):
                slug_candidate = f"{base_slug}-{index}"
                index += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    @property
    def is_live(self) -> bool:
        now = timezone.now()
        if self.is_draft or self.publish_at > now:
            return False
        if self.unpublish_at and self.unpublish_at <= now:
            return False
        return True


class ContactMessage(models.Model):
    """Store contact form submissions and make follow up easier."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    organization = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Message from {self.name} - {self.email}"


class SavedFilter(models.Model):
    """Store reusable search filters for publications/projects."""

    class FilterType(models.TextChoices):
        PUBLICATION = "publication", "Publications"
        PROJECT = "project", "Projects"

    name = models.CharField(max_length=120)
    filter_type = models.CharField(max_length=20, choices=FilterType.choices)
    query = models.CharField(max_length=255, blank=True)
    parameters = models.JSONField(blank=True, default=dict)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.filter_type})"


class AnalyticsDataset(models.Model):
    """Optional CSV datasets that feed analytics visualizations."""

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    csv_file = models.FileField(
        upload_to="analytics_uploads/",
        validators=[FileExtensionValidator(["csv"])],
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="analytics_uploads",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name


class Collaboration(models.Model):
    """Partnerships powering research impact."""

    class PartnerType(models.TextChoices):
        ACADEMIC = "academic", "Academic"
        CLINICAL = "clinical", "Clinical"
        INDUSTRY = "industry", "Industry"
        NGO = "ngo", "NGO / Philanthropy"

    name = models.CharField(max_length=255)
    partner_type = models.CharField(
        max_length=20, choices=PartnerType.choices, default=PartnerType.ACADEMIC
    )
    region = models.CharField(max_length=120)
    location = models.CharField(max_length=255, blank=True)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(blank=True, null=True)
    summary = models.TextField()
    grants = models.CharField(max_length=255, blank=True)
    responsibilities = models.TextField(blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    labs = models.ManyToManyField(
        LabExperience, blank=True, related_name="collaborations"
    )
    projects = models.ManyToManyField(
        Project, blank=True, related_name="collaborations"
    )

    class Meta:
        ordering = ["-start_year"]

    def __str__(self) -> str:
        return self.name

    @property
    def duration_label(self) -> str:
        end = self.end_year or "Present"
        return f"{self.start_year} – {end}"
