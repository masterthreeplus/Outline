# ... (အပေါ်က import တွေနဲ့ variable တွေ အတူတူပဲထားပါ)

@server.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# ဒီနေရာကို ပြင်လိုက်ပါ - 
# UptimeRobot ခေါ်ရင် ဒီ route က အလုပ်လုပ်မယ်၊ ဒါပေမဲ့ Telegram ဆီ Webhook သွားမချိတ်တော့ဘူး
@server.route("/")
def index():
    return "Bot is running!", 200

# --- BOT COMMANDS ---
# (သင့်ရဲ့ /start နဲ့ /getkey command တွေ ဒီကြားထဲမှာ ထည့်ပါ)

# အောက်ဆုံးက အပိုင်းကို ဒီလို ပြင်ပါ
if __name__ == "__main__":
    # App စတက်ချင်းမှာ တစ်ကြိမ်ပဲ Webhook ချိတ်မယ်
    try:
        bot.remove_webhook()
        bot.set_webhook(url=APP_URL + '/' + BOT_TOKEN)
        print("✅ Webhook set successfully")
    except Exception as e:
        print(f"❌ Webhook setup error: {e}")

    port = int(os.environ.get("PORT", 10000))
    server.run(host="0.0.0.0", port=port)
