"""Test sending an email using Python with smtp."""


import smtplib
from getpass import getpass


def send_email(user, pwd, recipients, subject, body):
    """Send an email using Python with smtp."""
    
    # Prepare the message
    message = f"From: {user}\nTo: {", ".join(recipients)}\nSubject: {subject}\n\n{body}"

    # Send the message
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(user, recipients, message)
        server.close()
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email.")
        print(e)


if __name__ == "__main__":
    # Get the email credentials
    user = input("Enter your email: ")
    pwd = getpass("Enter your password: ")

    to = input("Enter the recipient's email: ")

    send_email(user, pwd, [to], "Test email", "This is a test email.")
