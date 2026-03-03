from django import forms

from .models import AnalyticsDataset, ContactMessage, NewsPost


class ContactMessageForm(forms.ModelForm):
    """Allow visitors to send messages from the contact section."""

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "organization", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Full name",
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Email address",
                    "class": "form-control",
                }
            ),
            "organization": forms.TextInput(
                attrs={
                    "placeholder": "Institution or company",
                    "class": "form-control",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "How can I help you?",
                    "class": "form-control",
                }
            ),
        }


class NewsPostForm(forms.ModelForm):
    """Form used in the Django-powered news dashboard."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ("publish_at", "unpublish_at"):
            value = self.initial.get(field_name) or getattr(
                self.instance, field_name, None
            )
            if value:
                self.initial[field_name] = value.strftime("%Y-%m-%dT%H:%M")

    class Meta:
        model = NewsPost
        fields = [
            "title",
            "summary",
            "link",
            "publish_at",
            "unpublish_at",
            "is_draft",
            "is_featured",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "summary": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "link": forms.URLInput(attrs={"class": "form-control"}),
            "publish_at": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "unpublish_at": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "is_featured": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_draft": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class AnalyticsDatasetForm(forms.ModelForm):
    """Upload CSV datasets that power analytics visualizations."""

    class Meta:
        model = AnalyticsDataset
        fields = ["name", "description", "csv_file"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "csv_file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
