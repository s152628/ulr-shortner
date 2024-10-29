from flask import Flask, render_template, redirect, request, g
import random
import sqlite3
import logging
from functools import wraps
from collections import OrderedDict
import re

logging.basicConfig(
    filename="URL_shortner.log",
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG,
)


app = Flask(__name__)


def log_inputs_and_exceptions(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.debug(
                    f"Functie {func.__name__} werd aangeroepen met argumenten: {args} en keyword argumenten: {kwargs}"
                )
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(
                    f"Een fout is ontdekt in functie '{func.__name__}': {e}"
                )
                raise

        return wrapper

    return decorator


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

    return wrapper


@remember_recent_calls
def get_url_by_alias(alias):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT url FROM urls WHERE alias = ?", (alias,))
    result = cursor.fetchone()
    return result[0] if result else None


def random_alias(length=15):
    return "".join(chr(random.randint(ord("a"), ord("z"))) for _ in range(length))


# url controleren door behulp van regex
def is_url_valid(url):
    pattern = r"^https?://\w+\.\w+"
    text = url
    return re.match(pattern, text)


# Database connectie aanmaken
@log_inputs_and_exceptions(app.logger)
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
@log_inputs_and_exceptions(app.logger)
def pagecontent():
    app.logger.debug("Homepagina werd bezocht")
    return render_template("template.html")


# shorturl pagina waar de gebruiker naartoe wordt gestuurd als hij een alias en een url heeft ingevoerd


@app.route("/shorturl")
@log_inputs_and_exceptions(app.logger)
def controlpage():
    app.logger.debug("Shorturl pagina werd bezocht")
    url = request.args.get("url")
    errors = []
    if not url:
        errors.append("Url is required")
        return render_template("template.html", errors=errors)
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT alias FROM urls WHERE alias = ?", (url,))
    existing_alias = cursor.fetchone()
    if existing_alias:
        return redirect(f"/{existing_alias[0]}")
    if not is_url_valid(url):
        return render_template("template-404.html")

    # url en alias worden in de database opgeslagen
    alias = random_alias()
    cursor.execute("INSERT INTO urls VALUES (?, ?)", (alias, url))
    db.commit()
    return render_template("template-shorturl.html", alias=alias)


@app.route("/<alias>")
@log_inputs_and_exceptions(app.logger)
def redirect_to_url(alias):
    """Redirect to the original URL if the alias is found."""
    url = get_url_by_alias(alias)
    if url:
        return redirect(url)
    else:
        return render_template("template-404.html")
