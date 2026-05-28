from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ShortURL(db.Model):
    __tablename__ = "short_urls"

    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.Text, nullable=False)
    short_code = db.Column(db.String(12), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_clicks = db.Column(db.Integer, default=0)

    clicks = db.relationship(
        "ClickAnalytics",
        backref="short_url",
        lazy=True,
        cascade="all, delete-orphan"
    )


class ClickAnalytics(db.Model):
    __tablename__ = "click_analytics"

    id = db.Column(db.Integer, primary_key=True)
    short_url_id = db.Column(db.Integer, db.ForeignKey("short_urls.id"), nullable=False)
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
