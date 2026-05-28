# URL Shortener

A Flask-based URL Shortener project with:

- REST APIs
- SQLite database design
- Short URL redirects
- Click analytics
- In-memory caching

## Features

- Create short links from long URLs
- Redirect short URLs to original URLs
- Track total clicks
- Track click timestamp, IP address, and user agent
- View analytics for each short code
- Simple homepage for testing
- SQLite database included via SQLAlchemy
- Basic cache for faster redirects

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML/CSS

## Project Structure

```text
url_shortener/
├── app.py
├── models.py
├── utils.py
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   └── analytics.html
└── static/
    └── style.css
```

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## API Endpoints

### 1. Create Short URL

```http
POST /api/shorten
Content-Type: application/json
```

Body:

```json
{
  "long_url": "https://example.com"
}
```

Response:

```json
{
  "short_code": "aB12xY",
  "short_url": "http://127.0.0.1:5000/aB12xY",
  "long_url": "https://example.com"
}
```

### 2. Redirect

```http
GET /<short_code>
```

Example:

```text
http://127.0.0.1:5000/aB12xY
```

### 3. Analytics

```http
GET /api/analytics/<short_code>
```

Response:

```json
{
  "short_code": "aB12xY",
  "long_url": "https://example.com",
  "total_clicks": 5,
  "created_at": "2026-05-28T10:20:30",
  "clicks": [...]
}
```

## Why This Project Is Good

This project demonstrates backend fundamentals:

- REST API design
- Database relationships
- Redirect logic
- Analytics tracking
- Caching for performance
- Clean project structure
