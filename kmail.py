from wheezy.core.mail import MailMessage
from wheezy.core.mail import SMTPClient
from premailer import transform
from local_settings import *


def send_mail(email):
    try:
        content = file("email.html", "r")
        mail = MailMessage(
            subject='Welcome to wheezy',
            content=transform(content.read()),
            content_type='text/html',
            charset='utf-8',
            from_addr='no-reply@kax.io',
            to_addrs=[email])

        client = SMTPClient(
            host=host,
            port=port,
            use_tls=use_tls,
            username=username,
            password=password)
        client.send(mail)
        return True
    except:
        return False
