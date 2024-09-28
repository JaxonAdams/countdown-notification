import os
import ssl
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

    return images[int(datetime.now().timestamp()) % len(images)]


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
    date_diff = calculate_date_difference(current_date, "2025-09-16")

    aulani_image = select_aulani_image()

    # build the message body
    body_html = f"""
    <html>
        <body style="width: 80%; margin: 0 auto;">
            <h1 style="text-align: center; width: 100%; margin: 0 auto 0.5rem auto;">
                Disney Aulani Countdown
            </h1>
            <h2 style="text-align: center; margin: 0.5rem 1rem;">
                {date_diff["days"]} days ({date_diff["weeks"]} weeks) left until September 16, 2025!
            </h2>
            <img src="{aulani_image}" alt="Aulani Resort" style="width: 100%; border-radius=18px"/>
            <br/>
            <h3 style="margin: 0.5rem 1rem;"> - Jaxon</h3>
        </body>
    </html>
    """

    body_plain = f"""
    Countdown to 2025-09-16

    {date_diff["days"]} days ({date_diff["weeks"]} weeks) left until September 16, 2025!

    Don't miss out on the fun!

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
