import os
import imaplib
import email
import base64
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

IMAP_SCOPES = ['https://mail.google.com/']
SMTP_SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CREDENTIALS_PATH = 'credentials.json'
IMAP_TOKEN_PATH = 'token_imap.json'
SMTP_TOKEN_PATH = 'token_smtp.json'
EMAIL_ACCOUNT = 'eldaqidedaqi@gmail.com'

def get_gmail_credentials(token_path, scopes):
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, scopes)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return creds

def check_activation_tickets():
    creds = get_gmail_credentials(IMAP_TOKEN_PATH, IMAP_SCOPES)
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    auth_str = f"user={EMAIL_ACCOUNT}\1auth=Bearer {creds.token}\1\1".encode()
    imap.authenticate('XOAUTH2', lambda x: auth_str)
    imap.select('inbox')
    typ, data = imap.search(None, '(UNSEEN SUBJECT "Activation Ticket")')
    tickets = []
    for num in data[0].split():
        typ, msg_data = imap.fetch(num, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(decode=True).decode()
                else:
                    body = msg.get_payload(decode=True).decode()
                tickets.append({'id': num.decode(), 'subject': msg['subject'], 'from': msg['from'], 'body': body})
        imap.store(num, '+FLAGS', '\\Seen')
    imap.logout()
    return tickets

def send_email(subject, body, to_email):
    creds = get_gmail_credentials(SMTP_TOKEN_PATH, SMTP_SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    msg = EmailMessage()
    msg.set_content(body)
    msg['To'] = to_email
    msg['From'] = EMAIL_ACCOUNT
    msg['Subject'] = subject
    encoded_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    create_message = {'raw': encoded_msg}
    try:
        send_msg = service.users().messages().send(userId='me', body=create_message).execute()
        return True, send_msg.get("id")
    except Exception as e:
        return False, str(e)
