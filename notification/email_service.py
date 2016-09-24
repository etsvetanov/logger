import smtplib
from email.mime.text import MIMEText


class EmailService:

    @staticmethod
    def get_mime_msg(from_email, to_email, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        return msg

    def send(self, message, username, password):
        msg = self.get_mime_msg(message.from_email,
                                message.to_email,
                                message.subject,
                                message.body)

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(message.from_email, [message.to_email], msg.as_string())
        server.quit()


class Message:
    def __init__(self, to_email, from_email, subject, body):
        self.to_email = to_email
        self.from_email = from_email
        self.subject = subject
        self.body = body
