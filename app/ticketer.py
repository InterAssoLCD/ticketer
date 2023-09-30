from flask import Flask, render_template, request, abort, Response
from database import TicketSession
from dotenv import load_dotenv
from os import environ
from json import dumps
from datetime import date
from coder import render_ticket_html

app = Flask(__name__)

load_dotenv()


@app.route("/")
def index():
    return render_template("site/app.jinja2")


@app.route("/api/get/<ticket_uuid>")
def get_ticket(ticket_uuid: str):
    ts = TicketSession(environ["SESSION_ID"])
    ticket = ts.get_ticket(ticket_uuid)
    if ticket and ticket["used"] != 1:
        ts.use_ticket(ticket_uuid)
    ts.close()
    return dumps(ticket)


@app.route("/api/create", methods=["POST"])
def create_ticket():
    data: dict = request.get_json()

    if set(data.keys()) != {"nom", "prenom", "anniversaire"}:
        abort(404, "Mauvais format de données")
    try:
        date.fromisoformat(data["anniversaire"])
    except ValueError:
        abort(404, "Anniversaire : format invalide (doit être iso YYYY-MM-DD)")

    ts = TicketSession(environ["SESSION_ID"])

    ticket_uuid = ts.create_ticket(data["nom"], data["prenom"], data["anniversaire"])
    ticket = ts.get_ticket(ticket_uuid)
    with open(f"app/tickets/{ticket_uuid}.html", "w", encoding="utf-8") as file:
        file.write(render_ticket_html(ticket))

    ts.close()
    return dumps({"code": 200})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, ssl_context="adhoc", debug=True)
