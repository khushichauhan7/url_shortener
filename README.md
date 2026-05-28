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

## This project demonstrates backend fundamentals:

- REST API design
- Database relationships
- Redirect logic
- Analytics tracking
- Caching for performance
- Clean project structure
