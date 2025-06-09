from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from auth import Session, Player
from tkinter import filedialog

def export_to_pdf():
    session = Session()
    players = session.query(Player).all()
    session.close()

    # Вікно вибору шляху
    filepath = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Zapisz plik PDF jako"
    )

    if not filepath:
        return

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Statystyki graczy")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, "Nick")
    c.drawString(250, height - 80, "Wygrane")
    c.drawString(350, height - 80, "Przegrane")
    c.line(50, height - 85, 500, height - 85)

    y = height - 110
    for player in players:
        c.drawString(50, y, player.username)
        c.drawString(250, y, str(player.wins))
        c.drawString(350, y, str(player.losses))
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
