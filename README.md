AI Email Notifier Bot

A Python automation project that monitors a Gmail inbox in real time and forwards new emails directly to Telegram. Long emails are analyzed using Gemini Flash Lite, providing an AI-generated summary along with category and priority detection. The bot also supports Telegram commands for interacting with it without opening your inbox.

Features
Monitors a Gmail inbox using IMAP
Instant Telegram notifications for new emails
AI-powered email summaries (Gemini Flash Lite)
Automatic category and priority detection
Smart handling of short emails (configurable)
Supports both plain text and HTML emails
Detects and forwards email attachments
Handles multiple incoming emails correctly

Telegram commands:
/help
/latest
/status

Configurable settings through config.json
Secure credential management using confidentials.py
Logging system for debugging and monitoring
Technologies Used
Python
IMAP
Telegram Bot API
Google Gemini Flash Lite
BeautifulSoup
Requests

Project Structure:
AI-Email-Notifier-Bot/

├── main.py

├── confidentials.py
[confidentials_example.py](https://github.com/user-attachments/files/30010964/confidentials_example.py)

├── config.json

├── logs.txt

├── requirements.txt

└── README.md

How It Works
Connects securely to a Gmail inbox using IMAP.
Detects newly received emails.
Extracts the sender, subject, body, and attachments.
Generates an AI summary for longer emails.
Categorizes the email and assigns a priority level.
Sends the formatted notification (and attachments, if any) to Telegram.
Responds to Telegram commands such as /help, /latest, and /status.

Future Improvements:
Support for multiple Gmail accounts
More Telegram commands
Advanced filtering rules
Better email search and management features

Why I Built This:
I built this project to explore real-world Python automation by combining Gmail, the Telegram Bot API, and AI into a practical tool. It helped me work with APIs, IMAP, JSON configuration, logging, file handling, HTML parsing, and prompt engineering while solving a real problem.
