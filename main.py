import requests
import imaplib
import time
import email
from email.header import decode_header
from bs4 import BeautifulSoup
from confidentials import Chat_id, bot_token, app_password, api_key, Prompt_template
from google import genai
from datetime import datetime

client = genai.Client(api_key= api_key)

def sendMessage(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(url, data = {"chat_id": Chat_id, "text": message})
    logs(f"Message Sent\n")

def fetch_email_IDS():
    imap.noop()
    status, messages = imap.search(None, "ALL")
    return messages[0].split()

def get_email(latest_message):
    status, data = imap.fetch(latest_message, "(RFC822)")
    raw_email = None
    for item in data:
        if isinstance(item, tuple):
            raw_email = item[1]
            break
    if raw_email == None:
        return None
    logs(f"Email Received...\n")
    mail = email.message_from_bytes(raw_email)
    return mail

def format_message(Mail, text, summary):
    header = decode_header(Mail['Subject'])[0][0]
    if isinstance(header, bytes):
            subject = header.decode("utf-8")
    else:
        subject = header
    if summary == None:
        message1 =  f"📧 NEW EMAIL👤\n\n Sender:{Mail.get('From', 'Unkown')}\n\nSubject:{subject}\n\nReceived:{Mail.get('Date', 'Unkown')}\n\n Body:\n{text}\n ______________"
        return message1
    else:
        message2 =  f"📧 NEW EMAIL👤\n\n Sender:{Mail.get('From', 'Unkown')}\n\nSubject:{subject}\n\nReceived:{Mail.get('Date', 'Unkown')}\n\n {summary}\n ______________"
        return message2

def extract_body(Mail):
    content_type = Mail.get_content_type()

    if content_type == "text/plain":
        return Mail.get_payload()
    elif content_type == "multipart/alternative" or content_type == "multipart/mixed":
        for part in Mail.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload()
            elif part.get_content_type() == "text/html":
                html = part.get_payload()
                soup = BeautifulSoup(html, "html.parser")
                return soup.get_text()
    else:
        return None

def get_AI_summary(text, client):
    if len(text.split()) <= 20:
        return None
    prompt = Prompt_template.format(body=text)
    summary = client.models.generate_content(
        model="models/gemini-flash-lite-latest",
        contents = prompt
    )
    logs(f"Got AI summary...\n")
    return summary.text

def logs(log):
    with open("logs.txt", "a") as log_file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{log}  -->   {current_time}\n")

imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login("yrajbhar669@gmail.com",  app_password)
imap.select("INBOX")
logs(f"\nGmail account Logged in succesfully! \n")

email_ids = fetch_email_IDS()
if email_ids:
    last_seen = email_ids[-1]
else:
    last_seen = b"0"
print("Last seen:", last_seen)
while True:
    time.sleep(5)
    print("checking...")
    email_ids = fetch_email_IDS()
    if last_seen == b"0":
        last_seen = email_ids[-1]
    last_index = email_ids.index(last_seen)
    latest_messages = email_ids[last_index + 1 :]
    print("Latest Message/s: ", latest_messages)
    for latest_message in latest_messages:
        Mail = get_email(latest_message)
        if Mail is None:
            continue
        # print(Mail.keys())
        text = extract_body(Mail)
        if text is not None:
            summary = get_AI_summary(text, client)
        else: 
            summary = None
        message = format_message(Mail, text, summary)
        sendMessage(message)
        last_seen = latest_message
        # print(Mail.get_content_type())
        # print(Mail.is_multipart)