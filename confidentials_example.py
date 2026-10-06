# Rename this file to confidentials.py
# Add credentials here

Chat_id = "TELEGRAM_CHAT_ID"
bot_token = "TELEGRAM_BOT_TOKEN"
app_password = "GMAIL_APP_PASSWORD"
api_key = "GEMINI_API_KEY"

Prompt_template = '''Analyze the email below:
Return only:

Category: <category>
Priority: <Low|Medium|High>
Summary: <max 100 words>

Categories: (add relative emoji)
Work, Personal, Newsletter, Promotion, Social,
Finance, Shopping, Security, Travel, Event,
Support, Spam, Suspicious Other.
🚨 Spam/Phishing risk score:
Low / Medium / High
Ignore signatures and unsubscribe sections.
Email:
{body}'''
help = '''🤖 **Email Notifier Bot**\n
Welcome! I monitor your Gmail inbox and send notifications directly to Telegram.
📜Available Commands\n\n
🔹/help
Shows this help message and list all available commands.\n
🔹/status
Check whether the bot is running and view basic system information.\n
🔹/latest
Display the most recently received email notification.\n\n

📧Features
• Instant email notifications
• AI-generated email summaries
• Attachment forwarding
• Sender, subject, and timestamp tracking\n\n
🟢Bot Status: Online\n
Need assistance? Type a command to get started.
'''