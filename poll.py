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

def send_poll(question : str, options) -> None:
    """
        This function reads the chat id from the config.json file
        and send the question and options to every chat_id
        poll is valid till close_time. close_time is a unix timem stamp
    """
    poll = {
        "question" : question,
        "options" : json.dumps(options),
        "is_anonymous" : False,
        "type" : "quiz",
        "correct_option_id" : 0
    }

    for i in CHAT_ID:
        poll["chat_id"] = i
        try:
            for _ in range(20):
                r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPoll", data = poll)
                req_result = r.json()
                if r.status_code == 200 and req_result["ok"]:
                    print("Poll send successfuly")
                    break
                else:
                    print("error while sending the poll")
        except:
            print("Error in sending file to chat_id: ", i)

