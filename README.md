# Job Application Tracker API

A Django REST Framework backend that helps job seekers track and manage their job applications — from "Applied" to "Offered" — with real-time dashboard insights and upcoming interview alerts.

## Overview

This Project models a real workflow (job hunting) with status validation, per-user data isolation, aggregated analytics, and date-based filtering — built and tested end-to-end with Postman.

This project was built using Django REST Framework, with Claude AI used as a pair-programming assistant to speed up debugging, review code structure, and validate Django/DRF best practices throughout development. All architecture decisions, business logic, and implementation were written, tested, and debugged by me.

## Features

- Full CRUD for job applications scoped to the authenticated user
- JWT-based authentication using `djangorestframework-simplejwt`
- Strict user data isolation — users can only access their own applications
- Serializer-level business validation:
  - Status must be `interview` if an interview date is provided
  - Interview date is required if status is set to `interview`
- Dashboard endpoint with aggregated counts (applied, interview, offered, rejected)
- Upcoming interviews endpoint — surfaces interviews scheduled within the next 2 days
- Search and filter support via `django-filter` and DRF `SearchFilter`
- Pagination for list endpoints
- PostgreSQL database
- Fully tested via Postman across multiple user accounts

## Tech Stack

- Python
- Django
- Django REST Framework
- djangorestframework-simplejwt
- django-filter
- PostgreSQL

## Database Model

**JobApplication**

| Field | Type | Notes |
|---|---|---|
| user | ForeignKey(User) | Owner of the application |
| company_name | CharField | Company applied to |
| role | CharField | Position applied for |
| status | CharField (choices) | applied / interview / offered / rejected |
| applied_date | DateField | Auto-set on creation |
| interview_date | DateField | Optional, required only if status is "interview" |
| notes | TextField | Optional free-text notes |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/token/` | Obtain JWT access and refresh token |
| POST | `/api/token/refresh/` | Refresh JWT access token |
| GET | `/job/` | List authenticated user's job applications (paginated) |
| POST | `/job/` | Create a new job application |
| GET | `/job/<id>/` | Retrieve a single application |
| PUT | `/job/<id>/` | Update an application |
| DELETE | `/job/<id>/` | Delete an application |
| GET | `/dashboard/` | Get aggregated counts by status |
| GET | `/upcoming-interviews/` | Get interviews scheduled in the next 2 days |

### Filtering & Search

- `/job/?status=interview` — filter by exact status
- `/job/?company_name=Google` — filter by exact company
- `/job/?search=backend` — search across company name and role

## Business Logic

- **User isolation**: every queryset is scoped with `filter(user=request.user)`, so no user can ever see or modify another user's data — verified by testing with two separate accounts.
- **Status/date validation**: handled in the serializer's `validate()` method, enforcing that `interview_date` and `status="interview"` are always set together, preventing inconsistent data states.
- **Dashboard aggregation**: uses Django ORM `.filter().count()` per status to return a single summary object, avoiding the need for multiple client-side requests.
- **Upcoming interviews**: uses `datetime.date.today()` and `timedelta` to compute a rolling 2-day window and filters applications with `interview_date__range`.

## Setup

1. Clone the repository and create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure PostgreSQL in `settings.py` (or via environment variables) and create the database.
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Testing

This API was thoroughly tested using Postman, covering:

- JWT login and token refresh flows
- User isolation across two separate accounts
- Validation errors for inconsistent status/interview date combinations
- Pagination across multiple pages
- Filtering by status and company name
- Search across company name and role
- Dashboard accuracy against known data
- Upcoming interviews window accuracy
- Authorization checks — confirming one user cannot edit or delete another user's applications

## What I'd Add Next

- Automated test suite using Django's `TestCase`
- Email/notification reminders for upcoming interviews
- Rate limiting / throttling on write endpoints
- Deployment to Railway with CI/CD via GitHub

## Why This Project

I built this to genuinely track my own job applications during my fresher job search, which meant the features weren't arbitrary — they came from real needs: knowing my application status at a glance, not forgetting upcoming interviews, and keeping everything private to my own account.
