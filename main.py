from flask import Flask, render_template, redirect, request, g
import random
import sqlite3
import requests
import logging
from functools import wraps
from collections import OrderedDict

logging.basicConfig(
    filename="URL_shortner.log",
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG,
)


app = Flask(__name__)


def remember_recent_calls(func):
    cache = OrderedDict()

    @wraps(func)
    def wrapper(alias):
        if alias in cache:
            cache.move_to_end(alias)
            return cache[alias]

        result = func(alias)
        cache[alias] = result
        if len(cache) > 5:
            cache.popitem(last=False)

        return result


def random_alias(length=15):
    return "".join(chr(random.randint(ord("a"), ord("z"))) for _ in range(length))


def is_url_valid(url):
    try:
        response = requests.get(url, timeout=5)  # Set a timeout for the request
        return response.status_code == 200
    except requests.RequestException:
        return False


# Database connectie aanmaken
def get_db_connection():
    if "db" not in g:
        g.db = sqlite3.connect("urls.db")
        g.db.execute("CREATE TABLE IF NOT EXISTS urls (alias TEXT, url TEXT)")
    return g.db


@app.teardown_appcontext
def close_db_connection(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# homepagina aanmaken die de template.html laadt
@app.route("/")
def pagecontent():
    app.logger.debug("Homepagina werd bezocht")
    return render_template("template.html")


# shorturl pagina waar de gebruiker naartoe wordt gestuurd als hij een alias en een url heeft ingevoerd


@app.route("/shorturl")
def controlpage():
    app.logger.debug("Shorturl pagina werd bezocht")
    alias = random_alias()
    url = request.args.get("url")
    errors = []
    if not url:
        errors.append("Url is required")
    if errors:
        return render_template("template.html", errors=errors)
    elif not is_url_valid(url):
        return render_template("template-404.html")

    # url en alias worden in de database opgeslagen
    else:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO urls VALUES (?, ?)", (alias, url))
        db.commit()
        return render_template("template-shorturl.html", alias=alias)


# pagina die de gebruiker naar de url stuurt die bij de alias hoort
@remember_recent_calls
@app.route("/shorturl/<alias>")
def aliaspage(alias):
    app.logger.debug(f"Alias {alias} werd bezocht")
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT url FROM urls WHERE alias = ?", (alias,))
    url = cursor.fetchone()
    if url:
        return redirect(url[0])
    else:
        return f"Alias {alias} not found", 404
