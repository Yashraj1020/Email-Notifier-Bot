import requests
import imaplib
import time
import email
from email.header import decode_header
from bs4 import BeautifulSoup
from confidentials import Chat_id, bot_token, app_password, api_key, Prompt_template
from google import genai
from datetime import datetime
import json

client = genai.Client(api_key= api_key)

def sendMessage(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(
        url, 
        data= {"chat_id": Chat_id, "text": message},
        )
    logs("Message Sent\n")

def send_documents(file_name, file_data):
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    requests.post(
        url,
        data={"chat_id": Chat_id},
        files= {"document": (file_name, file_data)}
    )
    logs("Attachments sent \n")
    print(file_name, len(file_data))
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
        logs(f"Email Received...\n")
        return None
    logs(f"Email not found...\n")
    mail = email.message_from_bytes(raw_email)
    return mail

def format_message(Mail, text, summary, attachments, number_of_attachments):
    header = decode_header(Mail['Subject'])[0][0]
    if isinstance(header, bytes):
            subject = header.decode("utf-8")
    else:
        subject = header
    if summary == None:
        message1 =  f"📧 NEW EMAIL👤\n\n Sender:{Mail.get('From', 'Unkown')}\n\nSubject:{subject}\n\nReceived:{Mail.get('Date', 'Unkown')}\n\n Body:\n{text}\n\nIncluding {number_of_attachments} attachments:\n{'\n'.join(attachments)}\n ______________"
        return message1
    else:
        message2 =  f"📧 NEW EMAIL👤\n\n Sender:{Mail.get('From', 'Unkown')}\n\nSubject:{subject}\n\nReceived:{Mail.get('Date', 'Unkown')}\n\n {summary}\n\nIncluding {number_of_attachments} attachments:\n{'\n'.join(attachments)}\n ______________"
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
    if not summarize_short_emails and len(text.split()) <= minimum_words:
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

def process_attachments(Mail):
    folder = []
    for part in Mail.walk():
        file_name = part.get_filename()
        if file_name:
            file_data = part.get_payload(decode=True)
            folder.append((file_name, file_data))
    return folder

with open("config.json") as f:
    config = json.load(f)
    interval_time = config["Interval_time"]
    minimum_words = config["Minimum_words"]
    summarize_short_emails = config["Summarize_short_emails"]
    gmail = config["Gmail"]

imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(gmail,  app_password)
imap.select("INBOX")
logs(f"\nGmail account Logged in succesfully! \n")

email_ids = fetch_email_IDS()
emails_exist = bool(email_ids)
if email_ids:
    last_seen = email_ids[-1]
    last_index = email_ids.index(last_seen)
else:
    last_seen = b"0"
print("Last seen:", last_seen)
while True:
    print("checking...")
    time.sleep(interval_time)
    email_ids = fetch_email_IDS()
    if last_seen not in email_ids:
        if not emails_exist:
            latest_messages = email_ids
        else: 
            latest_messages = email_ids[last_index :]
    else:
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
        attachments = process_attachments(Mail)
        number_of_attachments = len(attachments)
        message = format_message(Mail, text, summary, [name for name, _ in attachments], number_of_attachments)
        sendMessage(message)
        for file_name, file_data in attachments:
            send_documents(file_name, file_data)
        last_seen = latest_message
        last_index = email_ids.index(last_seen)
        emails_exist = True
        # print(Mail.get_content_type())
        # print(Mail.is_multipart)