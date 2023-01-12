import smtplib
from email.mime.text import MIMEText # для текста на русском 
from app import app

def send_email(name, phone, topic):
    message = topic +'\nИмя: ' + name + '\nТелефон: ' + phone
    sender = app.config['EMAIL'] # наш маил
    password = app.config['PASSWORD_MAIL']  # наш токен

    server = smtplib.SMTP("smtp.yandex.ru", 587)
    server.starttls() # шифрованный обмен по TLS

    server.login(sender, password)
    msg = MIMEText(message)
    msg["Subject"] = 'Заявка с сайта ufa-zeh.ru'# тема письма
    msg["From"] = sender
    server.sendmail(sender, sender, msg.as_string())


