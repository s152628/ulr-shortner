from flask import Flask, render_template, abort, request
from markupsafe import escape

app = Flask(__name__)

aliasses = {
    "couldnthelpit": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley",
    "test": "https://www.w3schools.com/python/python_dictionaries.asp",
    "yaaas": "https://git-scm.com/docs/gitignore",
}


@app.route("/")
def pagecontent():
    with open("pagecontents.txt", "r") as file:
        pagecontents = file.read()
    return render_template("template.html", pagecontents=pagecontents)


@app.route(f"/shorturl/<alias>")
def aliasroute(alias):
    url = aliasses.get(alias)
    if url:
        return f"{url}"
    else:
        abort(404)
