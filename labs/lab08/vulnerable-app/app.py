from flask import (
    Flask,
    request,
    make_response,
    render_template_string,
    redirect,
    url_for,
    abort,
)
import sqlite3
import os
from markupsafe import escape

app = Flask(__name__)

DB_PATH = os.environ.get("APP_DB_PATH", "app.db")
FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
        """
    )
    cur.execute("DELETE FROM users")
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        ("admin", "admin123", "admin"),
    )
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        ("user", "user123", "user"),
    )
    conn.commit()
    conn.close()


@app.after_request
def add_security_headers(response):
    # --- CSP (корректный, без fallback-проблем) ---
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors 'none'; "
        "form-action 'self'"
    )

    # --- Anti-clickjacking / MIME sniffing / privacy ---
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    # --- Site isolation headers (то, что просит ZAP по Spectre) ---
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

    # --- Cache control (чтобы не кешировалось “на год” прокси/браузерами) ---
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    # --- Hide server version (Werkzeug/ Python versions) ---
    # В dev-сервере Flask это лучший вариант. В проде нужно убирать через reverse-proxy (nginx) или WSGI server.
    response.headers["Server"] = "WebServer"

    return response


@app.route("/")
def index():
    html = """
    <h1>DAST Demo App (Secured)</h1>
    <ul>
      <li><a href="/echo?msg=Hello">Echo (XSS fixed)</a></li>
      <li><a href="/search?username=admin">Search (SQLi fixed)</a></li>
      <li><a href="/login">Login</a></li>
      <li><a href="/profile">Profile</a></li>
      <li><a href="/admin">Admin panel</a></li>
      <li><a href="/files/secret.txt">Files (restricted)</a></li>
    </ul>
    """
    resp = make_response(html)
    resp.set_cookie(
        "session",
        "guest",
        httponly=True,
        samesite="Lax",
    )
    return resp


@app.route("/echo")
def echo():
    msg = escape(request.args.get("msg", ""))
    return render_template_string(
        """
        <h2>Echo</h2>
        <p>Сообщение: {{ msg }}</p>
        <a href="/">Назад</a>
        """,
        msg=msg,
    )


@app.route("/search")
def search():
    username = request.args.get("username", "")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT id, username, role FROM users WHERE username = ?", (username,))
    rows = cur.fetchall()
    conn.close()

    return render_template_string(
        """
        <h2>Поиск пользователя</h2>
        {% if rows %}
          <ul>
          {% for id, username, role in rows %}
            <li>{{ id }} – {{ username }} ({{ role }})</li>
          {% endfor %}
          </ul>
        {% else %}
          <p>Ничего не найдено</p>
        {% endif %}
        <a href="/">Назад</a>
        """,
        rows=rows,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template_string(
            """
            <h2>Login</h2>
            <form method="post">
              <input name="username">
              <input name="password" type="password">
              <button type="submit">Login</button>
            </form>
            """
        )

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT username, role FROM users WHERE username = ? AND password = ?",
        (username, password),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        abort(401)

    uname, role = row
    resp = make_response(redirect(url_for("profile")))
    resp.set_cookie("user", uname, httponly=True, samesite="Lax")
    resp.set_cookie("role", role, httponly=True, samesite="Lax")
    return resp


@app.route("/profile")
def profile():
    return render_template_string(
        """
        <h2>Profile</h2>
        <p>User: {{ user }}</p>
        <p>Role: {{ role }}</p>
        <a href="/">Назад</a>
        """,
        user=request.cookies.get("user", "guest"),
        role=request.cookies.get("role", "guest"),
    )


@app.route("/admin")
def admin():
    if request.cookies.get("role") != "admin":
        abort(403)

    return render_template_string(
        """
        <h2>Admin panel</h2>
        <p>Secure admin content</p>
        <a href="/">Назад</a>
        """
    )


@app.route("/files/<filename>")
def files(filename):
    # защита от traversal
    if "/" in filename or ".." in filename:
        abort(403)

    file_path = os.path.join(FILES_DIR, filename)
    if not os.path.isfile(file_path):
        abort(404)

    with open(file_path, encoding="utf-8", errors="ignore") as f:
        return f"<pre>{escape(f.read())}</pre>"


if __name__ == "__main__":
    init_db()
    # debug выключен, чтобы не светить лишнее
    app.run(host="0.0.0.0", port=8080, debug=False)

