import requests
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

def send_telegram_message(text):
    token = config["telegram"]["token"]
    chat_id = config["telegram"]["chat_id"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)
