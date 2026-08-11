from datetime import datetime
import json
import os
from google import genai
from google.oauth2.service_account import Credentials
import gspread
import telebot

# --- CONFIGURATION ---
TELEGRAM_TOKEN = os.getenv('8880709004:AAEYoQ7RodhthUj_SrwQCrkOJ6eXo3Gp4N0')
GEMINI_API_KEY = os.getenv('AQ.Ab8RN6ItA1ovWhUxHOjhNMJrA8RMFv85K3rqctnmO4bNSsVJZg')

# Render ke environment variable se JSON data uthayenge
service_account_info = json.loads(os.getenv('GOOGLE_CREDENTIALS_JSON'))

# Setup Clients
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client_ai = genai.Client(api_key=GEMINI_API_KEY)

# Google Sheets Setup
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',
]
creds = Credentials.from_service_account_info(
    service_account_info, scopes=scope
)
client_sheet = gspread.authorize(creds)
sheet = client_sheet.open('Expense Tracker').sheet1


@bot.message_handler(func=lambda message: True)
def chat_tracker(message):
  user_text = message.text.strip()
  try:
    all_records = sheet.get_all_records()
    prompt = f"""
        Tu ek smart, friendly aur Hinglish bolne wala personal finance assistant hai.
        Yeh raha user ka abhi tak ka sara expense data:
        {all_records}
        User ka message yeh hai: "{user_text}"
        1. Agar naya kharcha ho toh return kar: ADD|Amount|Category (Example: ADD|28|milk). Kuch aur mat likhna.
        2. Agar sawal ho toh friendly Hinglish mein jawab de.
        """
    response = client_ai.models.generate_content(
        model='gemini-2.5-flash', contents=prompt
    )
    ai_reply = response.text.strip()

    if ai_reply.startswith('ADD|'):
      parts = ai_reply.split('|')
      amount = parts[1]
      category = parts[2]
      date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      sheet.append_row([date, amount, category])
      bot.reply_to(
          message,
          f'✅ Bhai, entry ho gayi! ₹{amount} ({category}) add kar diya sheet'
          ' mein. 🚀',
      )
    else:
      bot.reply_to(message, ai_reply)
  except Exception as e:
    bot.reply_to(
        message,
        '❌ Kuch gadbad ho gayi bhai, dobara try kar ya format check kar.',
    )


bot.infinity_polling()
