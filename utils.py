from config import Config

from threading import Thread
import smtplib
from mimetypes import guess_type
from flask import render_template, current_app
from flask_login import current_user
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr, formataddr


def password_policy_check(user_password):
    import re

    check_errors = []

    min_length = Config.MINIMUM_PASSWORD_LENGTH
    password_complex = Config.PASSWORD_COMPLEX_PATTER
    

    if len(user_password) < min_length:
        err_msg = f"Password at least {min_length} chracters"
        check_errors.append(err_msg)

    if password_complex and not re.search(password_complex, user_password):
        err_msg = "Passowrd does not meet complexity rules"
        check_errors.append(err_msg)

    return check_errors if check_errors else False



def _operator():
    
    return current_user.fullname if current_user and current_user.is_authenticated else None


def _format_addr(s):
    
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))


def send_mail_async(app, msg):
    
    with app.app_context():
        try:
            with smtplib.SMTP(host=Config.MAIL_SERVER, port=Config.MAIL_PORT) as smtp:
                # 這裡加上送件者
                body = msg["Body"]
                body["From"] = _format_addr(Config.MAIL_DEFAULT_SENDER)
                
                smtp.starttls()
                
                smtp.login(Config.MAIL_DEFAULT_SENDER, Config.MAIL_DEFAULT_SENDER_PASSWORD)
                current_app.logger.debug("will send mail to {}".format(body["To"]))
                smtp.sendmail(from_addr=Config.MAIL_DEFAULT_SENDER,
                              to_addrs=msg["To"]+msg["Cc"]+msg["Bcc"],
                              msg=body.as_string())

                smtp.quit()

        except Exception as e:
            app.logger.error(str(e))


def create_mail_message(to: [str, list], subject: str, text: str = None, template: str = None, **kwargs):
    
    msg = {"To": [], "Cc": [], "Bcc": []}
    
    mail = None
    
    mime_text = None
    if template:
        html = render_template("{}".format(template), operator=_operator(), **kwargs)
        mime_text = MIMEText(html, "html", "utf-8")
    else:
        mime_text = MIMEText(text, "plain", "utf-8")

    if mail:
        mail.attach(mime_text)
    else:
        mail = mime_text

    mail["Subject"] = Header(subject, "utf-8").encode()
    recipients = []
    if type(to) == list:
        recipients += to
    else:
        recipients.append(to)
    msg["To"] = [_format_addr(recipient) for recipient in recipients]
    mail["To"] = ",".join(msg["To"])

    msg["Body"] = mail

    return msg


def send_mail(msgs):
    
    app = current_app._get_current_object()
    thread = Thread(target=send_mail_async, args=[app, msgs])
    thread.start()
    return thread


