from flask import Flask, request, jsonify, render_template
import logging
from datetime import datetime
import string
import random
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# إعداد اللوجينغ
logging.basicConfig(
    filename="not_recognized.log",
    encoding="utf-8",
    filemode="a",
    format="(%(asctime)s) | %(name)s | %(levelname)s | %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)
my_logging = logging.getLogger("Logging")

bot_handler = logging.FileHandler("bot_messages.log", encoding="utf-8")
bot_formatter = logging.Formatter("(%(asctime)s) | %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
bot_handler.setFormatter(bot_formatter)
bot_logging = logging.getLogger("BotLogger")
bot_logging.addHandler(bot_handler)
bot_logging.setLevel(logging.WARNING)


# تحميل بيانات المعرفة
def load_responses(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"⚠️ Warning: The file '{filename}' was not found.")
        return []

greetings = load_responses("greetings.txt")
about = load_responses("about.txt")

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('Home.html',
                            title='Home',
                            css_file='home.css')  # اسم ملف HTML اللي صممته

# API لاستقبال رسالة المستخدم
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_message = data.get('message', '').strip().lower()

    if user_message in ["hi", "hello", "hey"]:
        response = random.choice(greetings) if greetings else "Hello!"
    elif user_message in ["pass", "password"]:
        response = "Here is a strong and secure password generated for you:"
        response = generate_password()
    elif user_message == "date":
        response = datetime.now().strftime("%Y-%m-%d")
    elif user_message == "about":
        response = "\n".join(about) if about else "No info available."
    elif user_message == "help":
        response = """Available commands:
- hi / hello / hey
- pass / password
- date
- about
- exit"""
    elif user_message == "exit":
        response = "Goodbye 👋"
    else:
        bot_logging.warning(user_message)
        my_logging.warning(user_message)
        response = "I don't know what that is. Type 'help'."

    return jsonify({"response": response})

def generate_password():
    all_chars = string.ascii_letters + string.digits
    serial_list = []
    count = random.randint(8, 16)

    while len(serial_list) < count:
        char = random.choice(all_chars)
        if len(serial_list) == 0 and (char.islower() or char.isdigit()):
            continue
        serial_list.append(char)
    
    return "Here is a strong and secure password generated for you \n" + "Passowrd: " + "".join(serial_list)

if __name__ == "__main__":
    app.run(port=9000, debug=True)
