import smtplib
import ssl
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(send_to, msg):
    'Establishes a secure connection to an email service and sends an email'
    port = 465  # ssl port

    # create a secure SSL context
    context = ssl.create_default_context()

    # connect to smtp service and send an email
    print(' > Connecting to email service ... ')
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        print(' > Logging in ... ')
        server.login(FROM_ADDR, PW)
        print(' > Sending message ... ')
        server.sendmail(FROM_ADDR, send_to, msg.as_string())


def build_message():
    'Builds a MIME multipart message'
    # message data
    to_addr = input('Who would you like to send an email to? > ')
    
    # set up message object
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Testing ... '
    message['From'] = FROM_ADDR
    message['To'] = to_addr

    # define plain text and html versions of the message
    plain = '''\
    Hello, world!

    I'm testing out sending emails automatically. Don't mind lil' ol' me!

    - Jaxon
    '''
    html = '''\
    <html>
        <body style="width: 80%; margin: 0 auto; border: 1px solid black; border-radius: 18px;">
            <h1 style="text-align: center; width: 100%; margin: 0 auto 0.5rem auto; background: steelblue; color: white; border-radius: 18px 18px 0 0;">
            Hello, world!
            </h1>
            <i style="color: tomato; margin: 0.5rem 1rem; font-size: 1.2rem; text-align: center;">
            I'm testing out sending emails automatically. Don't mind lil' ol' me!
            </i>
            <br/>
            <h2 style="margin: 0.5rem 1rem;"> - Jaxon</h3>
        </body>
    </html>
    '''

    # convert to MIME objects
    as_txt = MIMEText(plain, 'plain')
    as_html = MIMEText(html, 'html')

    # attach to message object
    message.attach(as_txt)
    message.attach(as_html)
    # the email client will try to render the last part first, in this case the html version

    return to_addr, message


# !----------------------------------------------
if __name__ == '__main__':
    # pull email address and password from environment variables
    # mine are set in my virtual environment
    try:
        FROM_ADDR = os.environ['EMAIL_ADDRESS']
        PW = os.environ['EMAIL_PW']
    except KeyError:
        print('Email address and password not found.')
        sys.exit()

    try:
        msg = build_message()
        send_mail(*msg)
    except Exception as e:
        print(f'Sorry, something went wrong: {e}')
        sys.exit()
    else:
        print('Your email has been sent!')