from datetime import datetime
import os
from google import genai
from google.genai import types
from google.oauth2.service_account import Credentials
import gspread
import telebot

# --- CONFIGURATION ---
TELEGRAM_TOKEN = '8880709004:AAEYoQ7RodhthUj_SrwQCrkOJ6eXo3Gp4N0'
GEMINI_API_KEY = (
    'AQ.Ab8RN6ItA1ovWhUxHOjhNMJrA8RMFv85K3rqctnmO4bNSsVJZg'  # aistudio.google.com se free milegi
)
SERVICE_ACCOUNT_FILE = 'service_account.json'

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
creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=scope
)
client_sheet = gspread.authorize(creds)
sheet = client_sheet.open('Expense Tracker').sheet1


@bot.message_handler(func=lambda message: True)
def chat_tracker(message):
  user_text = message.text.strip()

  try:
    # Saara data sheet se utha lo taaki AI ko context mil jaye
    all_records = sheet.get_all_records()

    # System prompt taki AI samajh jaye ki wo ek smart finance buddy hai
    prompt = f"""
        Tu ek smart, friendly aur Hinglish bolne wala personal finance assistant hai.
        Yeh raha user ka abhi tak ka sara expense data (Google Sheet se):
        {all_records}

        User ka message yeh hai: "{user_text}"

        Tujhe decide karna hai:
        1. Agar user koi naya kharcha add kar raha hai (jaise "28 milk", "chai ke liye 50 diye"), toh usko extract karke sirf is format mein return kar: ADD|Amount|Category (Example: ADD|28|milk). Kuch aur mat likhna.
        2. Agar user koi sawal puch raha hai (jaise "dudh par kitna kharcha hua?", "is hafte kitna udaya?"), toh upar diye hue data ko analyze kar aur ekdam mast, friendly Hinglish/Hindi mein jawab de.
        """

    response = client_ai.models.generate_content(
        model='gemini-2.5-flash', contents=prompt
    )
    ai_reply = response.text.strip()

    # Agar AI ne expense add karne ka bola hai
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
      # Normal chat / query ka jawab jo AI ne diya hai
      bot.reply_to(message, ai_reply)

  except Exception as e:
    # Fallback agar seedha simple format mein bheja ho
    try:
      parts = user_text.split(' ', 1)
      if parts[0].isdigit():
        amount = parts[0]
        category = parts[1] if len(parts) > 1 else 'General'
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sheet.append_row([date, amount, category])
        bot.reply_to(
            message, f'✅ Saved: ₹{amount} for {category} (Fallback mode)'
        )
      else:
        bot.reply_to(
            message,
            'Bhai kuch samajh nahi aaya, thoda clearly likh ya dobara try kar!',
        )
    except:
      bot.reply_to(
          message, '❌ Error aa gaya bhai, code ya format check kar.'
      )


bot.infinity_polling()
