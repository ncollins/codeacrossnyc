import smtplib
import getpass
import argparse

from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import jinja2

import api


def create_email(json_data):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Community Board 09 Manhattan landlord action report'
    msg['From'] = 'test@test.com'
    msg['To'] = 'collins.nicholas@gmail.com'
    msg.preamble = 'the is the preamble'

    text = 'Hello!\nThis is the text version of the email.'
    html = '<h1>Hello!</h1><p>This is the HTML version of the email</>'

    part1 = MIMEText(text, 'plain')
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('/Users/nick/code/hackathons/codeacrossnyc'))
    template = env.get_template('email.html') 
    part2 = MIMEText(template.render(json_data), 'html')
    #part2 = MIMEText(template.render({'image_name': 'cid:image1'}), 'html')

    msg.attach(part1)
    msg.attach(part2) # part2 is the prefered type

    with open('test.png') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<image1>')
        msg.attach(img)

    return msg


def get_email_and_password():
    email = raw_input('email: ')
    password = getpass.getpass('password: ')
    return email, password

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='get email inputs')
    parser.add_argument('emails', metavar='E', type=str)
    args = parser.parse_args()

    with open(args.emails) as f:
        emails = f.read().split()

    email, password = get_email_and_password()

    json_data = api.final_data()
    
    msg = create_email(json_data)

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login(email, password)
    s.sendmail(email, ', '.join(emails), msg.as_string())
    s.quit()
