from flask import Flask, render_template, request, g
import sqlite3


app = Flask(__name__)


def get_db_connection():
    if "db" not in g:
        g.db = sqlite3.connect("urls.db")
        g.db.execute("CREATE TABLE IF NOT EXISTS urls (alias TEXT, url TEXT)")
    return g.db


@app.teardown_appcontext
def close_db_connection(error):
    if "db" in g:
        g.db.close()


@app.route("/")
def pagecontent():
    return render_template("template.html")


@app.route("/shorturl")
def controlpage():
    alias = request.args.get("alias")
    url = request.args.get("url")
    errors = []
    if not alias:
        errors.append("Alias is required")
    if not url:
        errors.append("Url is required")

    if errors:
        return render_template("template.html", errors=errors)
    else:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO urls VALUES (?, ?)", (alias, url))
        db.commit()
        return f"Alias: {alias} Url: {url}"


@app.route("/shorturl/<alias>")
def aliaspage(alias):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT url FROM urls WHERE alias = ?", (alias,))
    url = cursor.fetchone()
    if url:
        return f"Alias: {alias} Url: {url}"
    else:
        return f"Alias {alias} not found"
