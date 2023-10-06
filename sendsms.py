from scrapper import scrape
import os
from dotenv import load_dotenv

import smtplib
from email.message import EmailMessage

load_dotenv()
user = os.environ.get("EMAIL")
password = os.environ.get("PASS")
send_from = os.environ.get("NUMBER")


def sendsms():
    scrapped_data = scrape()
    filtered_data = scrapped_data[((scrapped_data['impact'] == 'High Impact Expected') | (scrapped_data['time'] == 'All Day')) & ((
        scrapped_data['currency'] == 'USD') | (
        scrapped_data['currency'] == 'EUR'))]
    return filtered_data.to_string(index=False, header=False)


def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = "FxNewsToSMS"  # doesnt work??

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()


def lambda_handler():
    data = sendsms()
    email_alert("Good Morning! Here's todays news.", data, send_from)


if __name__ == '__main__':
    data = sendsms()
    email_alert("Good Morning! Here's todays news.", data, send_from)
