from flask import Flask, render_template, redirect, request, g
import sqlite3


app = Flask(__name__)


# Database connectie aanmaken
def get_db_connection():
    if "db" not in g:
        g.db = sqlite3.connect("urls.db")
        g.db.execute("CREATE TABLE IF NOT EXISTS urls (alias TEXT, url TEXT)")
    return g.db


# homepagina aanmaken die de template.html laadt
@app.route("/")
def pagecontent():
    return render_template("template.html")


# shorturl pagina waar de gebruiker naartoe wordt gestuurd als hij een alias en een url heeft ingevoerd
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

    # url en alias worden in de database opgeslagen
    else:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO urls VALUES (?, ?)", (alias, url))
        db.commit()
        return f"Alias: {alias} Url: {url}"


# pagina die de gebruiker naar de url stuurt die bij de alias hoort
@app.route("/shorturl/<alias>")
def aliaspage(alias):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT url FROM urls WHERE alias = ?", (alias,))
    url = cursor.fetchone()
    if url:
        return redirect(url[0])
    else:
        return f"Alias {alias} not found", 404
