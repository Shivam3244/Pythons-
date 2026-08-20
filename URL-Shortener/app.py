from flask import Flask, render_template, request, redirect, abort
import sqlite3
import string
import secrets
from urllib.parse import urlparse

app = Flask(__name__)
DATABASE = "urls.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def generate_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


def valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    error = None

    if request.method == "POST":
        original_url = request.form.get("url", "").strip()

        if not valid_url(original_url):
            error = "Please enter a valid URL starting with http:// or https://."
        else:
            conn = get_db()

            # Reuse an existing short link for the same URL.
            existing = conn.execute(
                "SELECT short_code FROM urls WHERE original_url = ?",
                (original_url,)
            ).fetchone()

            if existing:
                code = existing["short_code"]
            else:
                code = generate_code()
                while conn.execute(
                    "SELECT 1 FROM urls WHERE short_code = ?", (code,)
                ).fetchone():
                    code = generate_code()

                conn.execute(
                    "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
                    (code, original_url)
                )
                conn.commit()

            conn.close()
            short_url = request.host_url.rstrip("/") + "/" + code

    return render_template("index.html", short_url=short_url, error=error)


@app.route("/<short_code>")
def redirect_url(short_code):
    conn = get_db()
    row = conn.execute(
        "SELECT original_url FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone()
    conn.close()

    if row is None:
        abort(404)

    return redirect(row["original_url"])


@app.errorhandler(404)
def not_found(error):
    return render_template("index.html", error="Short URL not found."), 404


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
