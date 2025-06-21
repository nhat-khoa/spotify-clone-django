# 🎵 Music Streaming Backend – Django + PostgreSQL + Chatbot (Ollama)

This is the **backend** for a full-stack music streaming platform built with **Django REST Framework**, **PostgreSQL**, and integrated with a local **chatbot using Ollama** for personalized music recommendations and assistance.

> 🔗 Frontend Repo: [Nuxt 3 – Music Streaming App](https://github.com/nhat-khoa/spotify-clone-nuxtjs)


---
## 📽️ Video Demo

👉 Watch At: [YouTube Video Demo](https://www.youtube.com/watch?v=3gcv87uj8qc)

---

## 🚀 Key Features

- 🔐 **Google OAuth2 Login**  
  Secure user authentication with Google using `google-auth` + `requests-oauthlib`.

- 🔑 **JWT Authentication**  
  Token-based security using `djangorestframework-simplejwt`.

- 🎧 **Music Streaming API**  
  Manage music data, albums, and user listening history using PostgreSQL.

- 💬 **Integrated Chatbot with Ollama**  
  Local chatbot (via Ollama) for music recommendations and user support.

- 🧾 **Interactive API Docs**  
  Swagger UI powered by `drf-yasg`.

---

## 🧪 Technology Stack

| Layer         | Tech Stack                                                                 |
|---------------|----------------------------------------------------------------------------|
| **Framework** | Django 5.1.6, Django REST Framework                                         |
| **Database**  | PostgreSQL with psycopg, Django ORM, and Django REST Framework           |
| **Auth**      | Google OAuth2, JWT (`simplejwt`)                                           |
| **Docs**      | Swagger (drf-yasg)                                                         |
| **Chatbot**   | Local LLM via [Ollama](https://ollama.com/) for AI-driven recommendations  |
| **Others**    | Mutagen (audio file metadata), yt-dlp, youtube-search-python               |

---

## 🗂️ Project Structure (simplified)
```
spotify-clone-backend/
├── apps/ # Django apps (modularized features)
│ ├── albums/ # Album models & APIs
│ ├── analytics/ # Track/user analytics
│ ├── artists/ # Artist-related endpoints
│ ├── authen/ # Authentication (Google OAuth2, JWT)
│ ├── categories/ # Genre & music categories
│ ├── core/ # Shared app config / utils
│ ├── group_sessions/ # Group listening sessions
│ ├── histories/ # Listening history
│ ├── interactions/ # Likes, favorites, follows
│ ├── playlists/ # Playlist features
│ ├── podcasts/ # Podcast management
│ ├── subscriptions/ # Premium subscriptions
│ ├── tracks/ # Track upload, stream, metadata
│ └── users/ # User profile & settings
│
├── main/ # Django project root (settings, URLs)
│
├── media/ # Uploaded media files
│
├── venv/ # Virtual environment (not tracked by Git)
│
├── manage.py # Django entry point
├── requirements.txt # Python dependencies
├── .env # Environment variables
├── .gitignore # Git ignore rules
├── spotify_songs.csv # Sample data (CSV import)
├── spotify-clone-db-img.png # DB schema visualization
└── README.md
```
---
## 📄 .env Configuration

Tạo file `.env` trong thư mục gốc và thêm các biến môi trường sau:

```env
# Django Settings
SECRET_KEY=django-insecure-m4pbmcmx-r!3_*u!p9gqaug7*vv%=2roge3d30gs1)7=j_g-7o
DEBUG=True

# PostgreSQL Database
DATABASE_URL=postgres://postgres:123456@localhost:5432/spotify_clone
DB_NAME=spotify_clone
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=5432

# MongoDB (Optional - for analytics, cache, or hybrid use)
MONGO_DATABASE_NAME=spotify_clone
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_URI=mongodb://localhost:27017

# OAuth
GOOGLE_CLIENT_ID=737867912492-rhok9ddk3cton3i5guo85ck0ak6p6aop.apps.googleusercontent.com

# Frontend App URL
FRONTEND_URL=http://localhost:3000
```

---

## ⚙️ Getting Started

```bash
# 1. Clone the project
git clone https://github.com/nhat-khoa/spotify-clone-backend.git
cd spotify-clone-backend

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # For Windows
# source venv/bin/activate  # For macOS/Linux

# 3. Install dependencies
cd main/
pip install -r requirements.txt

# 4. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 5. (Optional) Create superuser
python manage.py createsuperuser

# 6. Run development server
python manage.py runserver
```
---



