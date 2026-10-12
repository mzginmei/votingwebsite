# Comment Annotation Voting Website

A Django website for collecting human annotations on comments. Annotators decide whether each comment is **normal** or **has problems** (hate speech or another issue). When a comment has problems, annotators select every applicable problem category. The interface and annotation guidance include Kurdish text.

## Features

- Voter registration, login, logout, and password changes.
- Authenticated voting on batches of up to three comments at a time.
- Labels for no vote, normal, and problematic comments.
- Multiple problem categories can be selected for a problematic comment; at least one is required.
- Django admin management of comments, feedback, and problem categories.
- SQLite-backed local development settings and PostgreSQL-oriented deployment settings.

## Requirements

- Python 3.13 (the version used by the Docker image; Django 6 requires Python 3.12 or newer).
- pip

## Run locally

The development settings use SQLite. Run the following commands from the `website` directory.

```powershell
cd website
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ..\requirements.txt
python manage-debug.py migrate
python manage-debug.py createsuperuser
python manage-debug.py runserver
```

Open <http://127.0.0.1:8000/> in your browser. Register an annotator account from the site, or sign in with an existing account. The vote page requires authentication.

On macOS or Linux, create and activate the virtual environment with:

```bash
cd website
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
python manage-debug.py migrate
python manage-debug.py createsuperuser
python manage-debug.py runserver
```

## Add comments and problem categories

Create an admin user with `createsuperuser`, then visit <http://127.0.0.1:8000/admin/> and sign in. Add `Comment` entries and `FeedbackOption` entries before annotators start voting. Each feedback option should have a name and may include a description.

The website assigns each signed-in voter comments they have not yet labeled. A problematic label must include at least one problem category; normal comments do not require categories.

## Project layout

- `website/dsa/` — comment, feedback, and feedback-category models; voting views.
- `website/account/` — voter accounts, registration, and authentication routes.
- `website/templates/` — home, voting, and account pages.
- `website/website/settings-debug.py` — local development settings (SQLite, debug enabled).
- `website/website/settings.py` — deployment-oriented settings (PostgreSQL, debug disabled).
- `requirements.txt` — Python dependencies.

## Tests

Run the Django test suite from the `website` directory:

```powershell
python manage-debug.py test
```
