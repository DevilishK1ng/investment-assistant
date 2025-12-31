import smtplib
from email.mime.text import MIMEText

def send_email(text):
    msg = MIMEText(text)
    msg["Subject"] = "Alerta de inversión"
    msg["From"] = "alex.rojasrivera3@gmail.com"
    msg["To"] = "alex.rojasrivera3@gmail.com"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("alex.rojasrivera3@gmail.com", "gyxgurzsmxoqgdup")
    server.send_message(msg)
    server.quit()
