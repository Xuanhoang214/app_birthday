from flask import Flask, request
import pandas as pd
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Thay thế các giá trị này bằng thông tin của bạn
ACCESS_TOKEN = 'EAAGyJcEyek4BO3h02vTBeRQ63Kl53vmcDOnJaqFOvHYk1oRZBLg18F7kqE32cPWHynEGfTvqpZCXhZBjgAmLeqWZCbuqZCcdvZAdtEytxblVgjKJ23ItyZApzr7PRlbxrCsscAeGEQksB0ZAAb2g95ZB5tWvxC5a2vhEd9aLLf0ppcubFBH2vcsydRaHAm8bzUby9ULDeZAPdak7b45ZBViS0Jf6Nc1pyYybAZDZD'
VERIFY_TOKEN = 'YOUR_VERIFY_TOKEN'
RECIPIENT_ID = '100049365722962'  # ID của người dùng bạn muốn gửi tin nhắn

EXCEL_FILE = 'birthday.xlsx'

def send_message(recipient_id, message_text):
    url = 'https://graph.facebook.com/v2.6/me/messages'
    params = {'access_token': ACCESS_TOKEN}
    headers = {'Content-Type': 'application/json'}
    data = {
        'recipient': {'id': recipient_id},
        'message': {'text': message_text}
    }
    response = requests.post(url, params=params, headers=headers, json=data)
    return response.json()

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return 'Verification token mismatch', 403
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('message'):
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message'].get('text')
                    if message_text:
                        send_message(sender_id, "Hello! This is your birthday reminder bot.")
    return 'OK', 200

def check_birthdays():
    df = pd.read_excel(EXCEL_FILE)
    today = datetime.now().date()
    for index, row in df.iterrows():
        birthday = row['Birthday']
        name = row['Name']
        if isinstance(birthday, str):
            birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
        if birthday == today + timedelta(days=1):
            send_message(RECIPIENT_ID, f"Don't forget {name}'s birthday is tomorrow!")

@app.route('/check_birthdays', methods=['GET'])
def check_birthdays_route():
    check_birthdays()
    return 'Checked birthdays', 200

if __name__ == '__main__':
    app.run(debug=True)
