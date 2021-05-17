import smtplib
from email.message import EmailMessage

from app.models.gerente import Gerente
from app.models.incidencia import Incidencia


def send_mail( incidencia: Incidencia):
    
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("syskaoh", "AdriEsManco123")
    mails = ["syskaoh@gmail.com", incidencia.gerente.email]
    msg = EmailMessage()
    msg.set_content(
        f"""
    Usuario: {incidencia.gerente.nombre} {incidencia.gerente.apellidos}

    Cuerpo:
    {incidencia.cuerpo}
    
    """
    )

    msg["From"] = "syskaoh@gmail.com"
    msg["To"] = ",".join(mails)
    msg["Subject"] = f"Incidencia - {incidencia.gerente.username}: {incidencia.titulo}"
    server.sendmail("syskaoh@gmail.com", mails, msg.as_string())
    server.quit()


