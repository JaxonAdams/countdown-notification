import os
import ssl
import random
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def calculate_date_difference(start_date, end_date):
    "Calculate the number of days and weeks between two dates."
    
    # convert the dates to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # calculate the difference between the two dates
    delta = end_date - start_date

    return {
        "days": delta.days,
        "weeks": delta.days // 7,
    }


def select_aulani_image():
    "Select a random image of Disney's Aulani Resort."

    images = [
        "https://github.com/user-attachments/assets/e36593d9-29c0-4035-8fcc-b5d5d4e9797a",
        "https://github.com/user-attachments/assets/6bf12570-2dc6-429c-871b-d2714f680f06",
        "https://github.com/user-attachments/assets/f2a76fec-ccbb-4284-873c-ac689444ba29",
        "https://github.com/user-attachments/assets/cdfb819a-10cd-415c-982b-51b9efa3397b",
        "https://github.com/user-attachments/assets/43731db9-d5a4-4cdc-b514-29b6a60ac9d5",
        "https://github.com/user-attachments/assets/02759d66-a232-4ad3-9180-233b1086105a",
    ]

    return random.choice(images)


def select_aulani_text():
    "Select a random message about Disney's Aulani Resort."

    texts = [
        "enjoying the sun and sand at Aulani",
        "splashing around in the pools at Aulani",
        "relaxing in the lazy river at Aulani",
        "eating delicious food at Aulani",
        "watching the sunset at Aulani",
        "exploring the island of Oahu",
    ]

    return random.choice(texts)


def build_message(to_addr, subject, body_html, body_plain):
    "Build a MIME multipart message to send via SMTP."

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = os.getenv("EMAIL_ADDRESS")
    message["To"] = to_addr

    as_text = MIMEText(body_plain, "plain")
    as_html = MIMEText(body_html, "html")

    message.attach(as_text)
    message.attach(as_html)

    return message


def send_mail(messages):
    "Establish a secure connection to an email service and send an email."

    port = 465  # ssl port
    context = ssl.create_default_context()

    print(" > Connecting to email service ... ")
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        print(" > Logging in ... ")
        server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PW"))
        for addr, msg in messages:
            print(f" > Sending message to {addr} ... ")
            server.sendmail(os.getenv("EMAIL_ADDRESS"), addr, msg.as_string())


def main(event, context):
    """Main entry point for the function in AWS Lambda."""

    # get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # calculate the difference between the current date and the target date
    date_diff = calculate_date_difference(current_date, "2025-08-05")

    aulani_image = select_aulani_image()
    aulani_text = select_aulani_text()

    # build the message body
    body_html = f"""
    <html>
    <body style="margin: 0; padding: 0;">

    <table align="center" width="100%" style="padding: 40px; background-color: #f4f4f4;">
        <tr>
            <td align="center">
                <table width="364" cellspacing="0" cellpadding="0" style="background: rgba(255, 119, 0, 0.5); box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25); border-radius: 8px; margin-top: 80px;">
                    <tr>
                        <td style="padding: 20px;">
                            <h1 style="margin: 0; font-family: 'Inria Serif', serif; font-weight: 500; font-size: 36px; line-height: 44px; text-align: center; color: #000000;">
                                {date_diff['days']} days left!
                            </h1>
                        </td>
                    </tr>
                    <tr>
                        <td align="center" style="padding: 40px 0;">
                            <div style="width: 305px; height: 226px; background: url('{aulani_image}'); background-position: center; background-repeat: no-repeat; background-size: cover; border-radius: 12px;"></div>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 20px;">
                            <p style="margin: 0; font-family: 'Inria Serif', serif; font-weight: 500; font-size: 24px; line-height: 29px; text-align: center; color: #000000;">
                                In {date_diff['weeks']} weeks we'll be {aulani_text}!
                            </p>
                            <p style="margin: 0; font-family: 'Inria Serif', serif; font-weight: 500; font-size: 24px; line-height: 29px; text-align: center; color: #000000;">
                                - Jaxon
                            </p>
                            <p style="margin: 20px 0 0 0; text-align: center;">
                                (Beep boop -- this email was sent automatically.)
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>

    </body>
    </html>
    """

    body_plain = f"""
    Countdown to 2025-08-05

    {date_diff["days"]} days ({date_diff["weeks"]} weeks) left until August 5, 2025!

    - Jaxon
    """

    mailing_list = os.getenv("MAILING_LIST").split(",")

    # build the messages
    messages = []
    for addr in mailing_list:
        message = build_message(addr, f"{date_diff['days']} days to Aulani!", body_html, body_plain)
        messages.append((addr, message))

    # send the messages
    send_mail(messages)


if __name__ == "__main__":

    main(None, None)
