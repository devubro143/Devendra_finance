from datetime import datetime
import json
from google import genai
from google.oauth2.service_account import Credentials
import gspread
import telebot

# --- DIRECT KEYS LOADED (No environment variable lafda) ---
TELEGRAM_TOKEN = '8880709004:AAEyOq7RodhthUj_SrwQCrkOJ6Exo3Gp4N0'
GEMINI_API_KEY = 'AQ.Ab8RN6ItA1ovWhUxHOjhNMJrA8RMFv85K3rqctnmO4bNSsVJZg'

# Service Account credentials direct yahan daal diye hain
service_account_info = {
    'type': 'service_account',
    'project_id': 'expance-tracker-505204',
    'private_key_id': 'e501b7df8fc7372a0637da8e0f0702adf58b5a85',
    'private_key': (
        '-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC+CzAq3lhQeaE8\np4CyqZeJgnuxqxNXKRF0VsndEPbtbx24t0dm6XZs8PRkna8orRBmDnP/TO4vFnpl\njWOv1vwXqjJxbh7pweYNB0hqM2QWf0G55t+v9kqUCVG+hd4PaGiY6IrvzcUYclh+\nAM9uTOW6KjnUkqc1LqCZHkuGrXUlqCLGZrTWVYl4l/3FImAJmIAN4YGd5cLj/zyL\nZknT1url3eoiytXkP24k302H5+PnYOnendjpQoutMzVwUEqNWX7vDb7/C5DhMviO\nJ0Y2Rww6idz0+kMKDIydc4tAAZXDcGJiq0mJ3iQs/1q/AKpDcW5oMtiriyqxGier\nl5kVWenTAgMBAAECggEALrScNWToqnqB/GCkOgSBCBwH303OloSy0/dCbDCvpwHA\nebWdeDbXUoXTYmj4c9Q4rARQUMWs4eix0wRxI/V/hidfd04bjdKIAdqw2tzfc8H5\nusD5Z4rtoD08GElZHktILZA1GSNmlZAAnJMBZ7fBW8Pl647RRjo74PW3lRVLLaIc\n4fV+4C/N7xyz0JKDp8ol4c61TkRojdpp1AnO1SPZf2/Q4xc8QElCWs4D4jQWnRWu\n99UMH7mTL0gDkaLJ+j9yzA38RGYm8/vwey30q6vLpg1lQa3jfkMwZYPSQYBLwEAW\nxeQR07Z7BwYpQwViD9rHzlw+iDhAV31aq0siGDpO5QKBgQDefcp5curAzY8bBC5x\nNbwBPhwEi3iZ0VtOFmYQxO3DL+4y4sPv5yqf+3+8W8eSngd70wUG8x1MeLDyglms\nutMY+1lFDKc8t5IFpPWxecFob0kL/gp+3ctMTJFDTMmsoMenZZxf2YnE9uCG2ROf\n2Kx8PEjdnFfDuw8Pd2e4HvHLrQKBgQDaql6YzbsIIo6UvZgNh8VbziopIIuFbgxm\ntJVeQmvFgPjPYw5KrZQLTDMXlAbv+LSTB+a797EoNV81i1OAG4lENWIflQngj9iW\nSyJ/8d0PkSi/XleLdb8tsVGLS/BkBUwPE73liTFy0yTrKhP22wA0eNNC+zGEi1my\nYhvIRek7fwKBgFpCl9B7UUcUXVjtclXVIcczRjSFzFBCgZMFPTTSX06O9EhKfIin\ntEAgzGpCpY0SdSDDs8dk+17Zm5dWUEDlrdv1o/qCLppQMnn9uPrd1RukAfNOhT2A\nhwgWC9xMm4hf1X9Qloa//sccDGxIRlDTmu3vmvPkiCpMiciRfU9RpnAlAoGBAKHT\n8Ip5x29v08G0xvFMh/03iPBDC77GARuJjfnigkv69SjWkF8oMyZhUHaksLWshEdE\nU7jMySmOxlWkNTncJyx5rZLeBB9TleE03eV+pDG/Jj7qnTOzArfYQRcsLk53tSB7\nZdCYRiZKqUn5LClHTtGGkiNCMBV94/YmsZT4WHIVAoGBAKyFMRhbchA3zgJ+hjjW\nIup2z3N+3Uqv96lIakSBn4j9VbdbgJCi2Ikul39yarBZWvwt1yob3JKSv4xIbpUG\nl6TY/jzttXu2GaIpTm7X4Nqaj06Zagc9oV1hnuuENb9a/2/2saYBTfsByxbvob1b\nMcawKX9DOv1FHncfFnjDmEUk\n-----END PRIVATE KEY-----\n'
    ),
    'client_email': (
        'finance-bot@expance-tracker-505204.iam.gserviceaccount.com'
    ),
    'client_id': '117013801784257347009',
    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
    'token_uri': 'https://oauth2.googleapis.com/token',
    'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
    'client_x509_cert_url': (
        'https://www.googleapis.com/robot/v1/metadata/x509/finance-bot%40expance-tracker-505204.iam.gserviceaccount.com'
    ),
    'universe_domain': 'googleapis.com',
}

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
