from flask import Flask, request, jsonify, redirect, render_template, url_for
from models import db, ShortURL, ClickAnalytics
from utils import generate_short_code, is_valid_url

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///url_shortener.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Simple in-memory cache:
# key = short_code, value = long_url
url_cache = {}


@app.before_request
def create_tables():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()

    if not data or "long_url" not in data:
        return jsonify({"error": "long_url is required"}), 400

    long_url = data["long_url"].strip()

    if not is_valid_url(long_url):
        return jsonify({"error": "Please enter a valid http or https URL"}), 400

    existing_url = ShortURL.query.filter_by(long_url=long_url).first()
    if existing_url:
        short_url = request.host_url + existing_url.short_code
        return jsonify({
            "short_code": existing_url.short_code,
            "short_url": short_url,
            "long_url": existing_url.long_url
        }), 200

    short_code = generate_short_code()

    while ShortURL.query.filter_by(short_code=short_code).first():
        short_code = generate_short_code()

    new_url = ShortURL(long_url=long_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()

    url_cache[short_code] = long_url

    short_url = request.host_url + short_code

    return jsonify({
        "short_code": short_code,
        "short_url": short_url,
        "long_url": long_url
    }), 201


@app.route("/<short_code>")
def redirect_short_url(short_code):
    long_url = url_cache.get(short_code)
    short_url_record = None

    if not long_url:
        short_url_record = ShortURL.query.filter_by(short_code=short_code).first()

        if not short_url_record:
            return render_template("index.html", error="Short URL not found"), 404

        long_url = short_url_record.long_url
        url_cache[short_code] = long_url
    else:
        short_url_record = ShortURL.query.filter_by(short_code=short_code).first()

    if short_url_record:
        click = ClickAnalytics(
            short_url_id=short_url_record.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent")
        )

        short_url_record.total_clicks += 1

        db.session.add(click)
        db.session.commit()

    return redirect(long_url)


@app.route("/api/analytics/<short_code>")
def api_analytics(short_code):
    short_url_record = ShortURL.query.filter_by(short_code=short_code).first()

    if not short_url_record:
        return jsonify({"error": "Short URL not found"}), 404

    clicks = []
    for click in short_url_record.clicks:
        clicks.append({
            "clicked_at": click.clicked_at.isoformat(),
            "ip_address": click.ip_address,
            "user_agent": click.user_agent
        })

    return jsonify({
        "short_code": short_url_record.short_code,
        "long_url": short_url_record.long_url,
        "total_clicks": short_url_record.total_clicks,
        "created_at": short_url_record.created_at.isoformat(),
        "clicks": clicks
    })


@app.route("/analytics/<short_code>")
def analytics_page(short_code):
    short_url_record = ShortURL.query.filter_by(short_code=short_code).first()

    if not short_url_record:
        return render_template("index.html", error="Short URL not found"), 404

    return render_template("analytics.html", url=short_url_record)


@app.route("/api/cache")
def cache_status():
    return jsonify({
        "cached_items": len(url_cache),
        "cached_short_codes": list(url_cache.keys())
    })


if __name__ == "__main__":
    app.run(debug=True)
