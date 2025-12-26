import os
import requests
import telebot
from flask import Flask, request
import urllib3

# SSL Error မတက်အောင် Warning ပိတ်ထားခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Configuration (Environment Variables) ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
OUTLINE_API_URL = os.environ.get('OUTLINE_API_URL')
APP_URL = os.environ.get('APP_URL')

# --- အစီအစဉ်မှန်အောင် ဤနေရာတွင် အရင် Define လုပ်ရပါမည် ---
bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__) # <--- ဒီကောင်က route တွေရဲ့ အပေါ်မှာ ရှိနေရပါမယ်

# --- Flask Routes ---

@server.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def index():
    return "Bot is running!", 200

# --- Telegram Bot Handlers ---

@bot.message_handler(commands=['start'])
def start(message):
    welcome_msg = (
        "👋 မင်္ဂလာပါ! Outline VPN Bot မှ ကြိုဆိုပါတယ်။\n\n"
        "Key ထုတ်ယူရန် /getkey ကို နှိပ်ပါ။"
    )
    bot.reply_to(message, welcome_msg)

@bot.message_handler(commands=['getkey'])
def create_key(message):
    try:
        # Outline API သို့ Key အသစ်တောင်းခြင်း
        response = requests.post(f"{OUTLINE_API_URL}/access-keys", verify=False, timeout=10)
        
        if response.status_code == 201:
            data = response.json()
            key = data['accessUrl']
            key_id = data['id']
            
            # Key ကို နာမည်ပေးခြင်း (Optional)
            requests.put(f"{OUTLINE_API_URL}/access-keys/{key_id}/name", 
                         data={'name': f"User_{message.from_user.id}"}, verify=False)
            
            bot.reply_to(message, f"✅ *VPN Key ရပါပြီ* -\n\n`{key}`", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Server မှ Key ထုတ်ပေးလို့ မရသေးပါ။")
    except Exception as e:
        bot.reply_to(message, "❌ Connection Error: Outline Server နဲ့ ချိတ်ဆက်လို့ မရပါ။")

# --- Main Logic ---

if __name__ == "__main__":
    # Webhook Setup
    try:
        bot.remove_webhook()
        bot.set_webhook(url=APP_URL + '/' + BOT_TOKEN)
        print("✅ Webhook set successfully")
    except Exception as e:
        print(f"❌ Webhook setup error: {e}")

    # Port Setup for Render
    port = int(os.environ.get("PORT", 10000))
    server.run(host="0.0.0.0", port=port)
