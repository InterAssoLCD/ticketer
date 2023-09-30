import base64
from io import BytesIO
import qrcode
import jinja2


def render_ticket_html(infos: dict):
    """
    Render html page using jinja
    """
    template_loader = jinja2.FileSystemLoader(searchpath="app/templates")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("ticket.jinja2")
    output_text = template.render(
        nom=infos["nom"],
        prenom=infos["prenom"],
        anniversaire=infos["anniversaire"],
        uuid=infos["uuid"],
        image=_get_base64_str(_generate_qr(infos["uuid"])),
    )

    return output_text


def _generate_qr(data: str):
    img = qrcode.make(data)
    return img


def _get_base64_str(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


if __name__ == "__main__":
    from database import TicketSession

    ts = TicketSession("up")
    ticket = ts.get_ticket("2d221ef4-30e2-4394-81d5-ace1f3c84f97")
    with open("test.html", "w", encoding="utf-8") as file:
        file.write(render_ticket_html(ticket))
