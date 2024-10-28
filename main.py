from flask import Flask, render_template, request


app = Flask(__name__)


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
        return f"Alias: {alias} Url: {url}"
