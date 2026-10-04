# Goal Tracker (YouTube Playlist & Progress Tracker)

A Django web application designed to help learners and developers track their progress across YouTube playlists, monitor completion rates, and manage learning goals without distractions.

---

## Features

- **YouTube Playlist Integration**: Easily add any YouTube playlist via its URL. The app automatically fetches videos, metadata, and thumbnails using the YouTube Data API v3.
- **Progress & Watch Tracking**: Mark individual videos as watched or unwatched to track your study progress.
- **Visual Dashboard**: View playlists, video counts, and completion status in one centralized dashboard.
- **User Authentication**: Built-in login and logout authentication views.
- **Clean Structure**: Standard Django project architecture with modular models and views.

---

## Tech Stack

- **Backend**: Python 3.10+ / Python 3.11+ & Django 5.1
- **API**: YouTube Data API v3 (via `requests`)
- **Database**: SQLite (default, easily switchable to PostgreSQL or MySQL)
- **Configuration**: `python-decouple` for environment variable management

---

## Project Structure

```text
goal-tracker/
├── goal_tracker/               # Main Django project directory
│   ├── goal_tracker/           # Project settings & URL routing
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── tracker/                # Main application (playlists & video models)
│   │   ├── models.py           # YouTubePlaylist & YouTubeVideo models
│   │   ├── views.py            # Playlist & video dashboard views
│   │   └── forms.py
│   ├── templates/              # HTML templates (Dashboard, Playlist views, Auth)
│   ├── static/                 # Static CSS & styles
│   └── manage.py
├── .env.example                # Sample environment variables configuration
├── .gitignore                  # Git ignore rules (virtualenvs, secrets, caches)
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## Getting Started

### 1. Prerequisites

- Python 3.10 or higher
- Git
- A Google Cloud Platform account with **YouTube Data API v3** enabled (to obtain an API key)

### 2. Clone the Repository

```bash
git clone https://github.com/Kaditya67/goal-tracker.git
cd goal-tracker
```

### 3. Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv myenv
.\myenv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the `goal_tracker` directory or set environment variables:

```env
# Optional: Provide a YouTube Data API v3 key to enable automatic playlist fetching
YOUTUBE_API_KEY=your_youtube_api_key_here
```

> **Note**: A template is provided in [`.env.example`](.env.example).

### 6. Run Migrations & Start Development Server

```bash
cd goal_tracker
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to access the application.

---

## License

This project was built for educational and practice purposes. Feel free to use and adapt it for your own learning goals.
