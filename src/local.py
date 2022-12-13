import smtplib
from email.message import EmailMessage

msg = EmailMessage()

msg['Subject'] = 'Hello Python World!'
msg['From'] = 'J. B. Goode <jgoode@example.com>'
msg['To'] = 'Pump King <peter.pumpking@example.com>'

msg.set_content("""Hello World,
    I am writing to tell you that I am alive!

Yours very truly,
Johnny B. Bad
""")


smtp = smtplib.SMTP('localhost:8025')
smtp.send_message(msg)
smtp.quit()

print(msg)

