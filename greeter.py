from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def form():
    return """
        <form action="/greet">
            <label for="name">Vul uw naam in:</label>
            <input type="text" id="voornaam" name="voornaam">
            <input type="text" id="achternaam" name="achternaam">
            <button type="submit">Submit</button>
        </form>
    """


@app.route("/greet")
def greet():
    voornaam = request.args.get("voornaam")
    achternaam = request.args.get("achternaam")
    return f"Hallo, {voornaam} {achternaam}!"
