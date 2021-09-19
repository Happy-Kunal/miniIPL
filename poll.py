import json
import requests
import time

try:
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    TOKEN = config["telegram_bot_token"]
    CHAT_ID = config["chat_id"]
except:
    print("Error parsing config file")
    sys.exit(2)

# r = requests.post(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()
# print(r)

def send_poll(question : str, options, close_time : int) -> None:
    """
        This function reads the chat id from the config.json file
        and send the question and options to every chat_id
        poll is valid till close_time. close_time is a unix timem stamp
    """
    poll = {
        "question" : question,
        "options" : json.dumps(options),
        "close_date" : close_time
    }

    for i in CHAT_ID:
        poll["chat_id"] = i
        try:
            r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPoll", data = poll).json()
        except:
            print("Error in sending file to chat_id: ", i)

