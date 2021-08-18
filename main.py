import smtplib
import logging
import os
from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from utils import get_contacts, get_template


def main():
    config = ConfigParser()
    config.read("config.cfg")

    input_folder = config.get("config", "input_folder")
    email_list = config.get("config", "email_list")
    body_template = config.get("config", "body_template")
    smtp_host = config.get("smtp", "host")
    smtp_port = config.get("smtp", "port")
    smtp_email = config.get("smtp", "email")
    smtp_password = config.get("smtp", "password")
    subject = config.get("smtp", "email_subject")
    log_output = "log.txt"

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s - %(message)s",
                        handlers=[
                            logging.FileHandler(log_output, mode="w"),
                            logging.StreamHandler()
                        ])

    if not os.path.exists(input_folder) or not os.listdir(input_folder):
        logging.error("Input folder doesn't exist or empty")
        return

    try:
        logging.info("Connecting to SMTP server ...")

        smtp_server = smtplib.SMTP(host=smtp_host, port=smtp_port)
        smtp_server.starttls()
        smtp_server.login(smtp_email, smtp_password)

        logging.info("Connected to SMTP server")
    except Exception as e:
        logging.error(f"Failed to connect to SMTP server: {e}")
        return

    names, emails = get_contacts(email_list)
    email_body_template = get_template(body_template)

    for name, email in zip(names, emails):
        logging.info(f"Sending email to {name} ({email}) ... ")

        try:
            msg = MIMEMultipart()

            message = email_body_template.substitute(NAME=name.title())

            msg['From'] = smtp_email
            msg['To'] = email
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            with open(f"{input_folder}/{name.title()}.png", 'rb') as fp:
                img = MIMEImage(fp.read())
                img.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=f"{name.title()}.png")
                msg.attach(img)

            smtp_server.send_message(msg)
            del msg

            logging.info(f"Success sending email to {name} ({email})")
        except Exception as e:
            logging.error(f"Failed sending email: {e}")

    smtp_server.quit()


if __name__ == '__main__':
    main()
