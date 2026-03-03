# Genomics & Bioinformatics Portfolio

A Django-powered, multi-section portfolio for genomics, bioinformatics, computational biology, and modeling work. The site provides a sticky navigation bar with dedicated pages for Research, Projects, Skills, Labs Experience, News, About/CV, and Contact, plus a landing page that highlights featured work.

## Key Features

- **Dynamic Research hub** – filter publications by topic or year, link out to DOIs, GitHub, or Google Scholar.
- **Project gallery** – cards grouped by project type (genomics pipelines, bioinformatics tools, modeling simulations, and data resources).
- **Interactive skills** – progress bars and a Chart.js visualization driven by database entries.
- **Labs experience timeline** – highlight responsibilities, techniques, and downloadable lab-specific reports.
- **News CMS** – manage announcements via Django admin or the `/news/manage/` form (login required).
- **About/CV & Contact** – downloadable CV placeholder plus a form that stores messages in the database.
- **Global search & saved filters** – combine publication/project queries with reusable saved filters.
- **Analytics dashboard** – Plotly-powered charts, CSV uploads, and a Leaflet collaboration map.

## Getting Started

```bash
cd /home/boi-kone/genomics_portfolio
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/` for the main site or `http://127.0.0.1:8000/admin/` for the admin.

### Create a superuser

```bash
source .venv/bin/activate
python manage.py createsuperuser
```

Use this account to log into the admin dashboard or the `/news/manage/` form.

## Managing Content

All sections pull content from the `website` app models:

| Section/Page | Model | Notes |
| --- | --- | --- |
| Research (`/research/`) | `Publication` | Add topics, year, links, and featured flag |
| Projects (`/projects/`) | `Project` | Use `project_type` to enable button filters |
| Skills (`/skills/`) | `Skill` | Set proficiency (0-100) for progress bars + charts |
| Labs Experience (`/labs/`) | `LabExperience` | Includes duration helper and report links |
| News (`/news/`) | `NewsPost` | Manage via admin or `/news/manage/` (login required) |
| Contact (`/contact/`) | `ContactMessage` | Stores submissions from the contact form |

Fixtures can be added later under `website/fixtures/`.

## Front-end Notes

- Styles live in `static/website/css/styles.css`; feel free to replace the hero background image or add more breakpoints.
- Interactivity (filters + charts) is handled in `static/website/js/main.js`.
- Smooth scrolling is enabled via CSS and works with the sticky Bootstrap navbar.
- Replace `static/website/docs/Genomics_CV_placeholder.pdf` with your actual CV to power the download button.

## Next Steps

- Add sample data through the admin to fully populate the sections.
- Configure email (see below) if you want contact messages to send notifications in addition to being stored.
- Deploy to your platform of choice (Railway, Fly.io, Render, etc.) using `DEBUG=False` and proper `ALLOWED_HOSTS`.
- Run ingestion commands to keep Research/News fresh:
  - `python manage.py sync_publications --query "computational biology"`
  - `python manage.py sync_news https://example.com/feed.xml`

### Email notifications

Contact form submissions trigger `send_mail` using the SMTP values below. Create a `.env` (or set real environment variables) before running the server:

```bash
export DJANGO_EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
export DJANGO_EMAIL_HOST="smtp.gmail.com"
export DJANGO_EMAIL_PORT="587"
export DJANGO_EMAIL_USE_TLS="True"
export DJANGO_EMAIL_USER="you@example.com"
export DJANGO_EMAIL_PASSWORD="app-password-or-token"
export DJANGO_DEFAULT_FROM_EMAIL="Portfolio Bot <you@example.com>"
export DJANGO_CONTACT_RECIPIENT_EMAIL="your-inbox@example.com"
```

Without those variables, Django falls back to the console email backend so you can still see the rendered message in the terminal during development.

### Live ingestion

Two management commands populate dynamic sections without manual data entry:

```bash
python manage.py sync_publications --query "genomics" --rows 25
python manage.py sync_news https://example.com/rss.xml --limit 15 --publish
```

Schedule them via cron (or a GitHub Actions workflow) to keep publications and news up to date.

## Sample data & tests

- Load demo content: `python manage.py loaddata website/fixtures/sample_data.json`
- Run the Django system check: `python manage.py check`
- Execute the pytest suite (uses factory-boy + pytest-django): `pytest`

## Continuous Integration

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs the following on every push/PR:

1. `python manage.py check`
2. `pytest`
3. `ruff .`
4. `black --check .`

## Automation & Ops

- Scheduled ingestion (`.github/workflows/ingestion.yml`) runs `sync_publications` and `sync_news` daily at 03:00 UTC. Populate the following repository secrets: `DJANGO_SECRET_KEY`, SMTP settings (`DJANGO_EMAIL_*`), `DATABASE_URL`, `CROSSREF_QUERY`, and `NEWS_FEED_URL`.
- Release checklist: `docs/RELEASE_CHECKLIST.md`
- Deployment guide (Render/Fly/Railway ready): `docs/DEPLOYMENT_GUIDE.md`

Happy showcasing! 🎉

