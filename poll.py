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

def get_last_update_message_id():
    r = requests.post(f"https://api.telegram.org/bot{TOKEN}/getUpdates")
    if r.status_code == 200 and r.json()["ok"]:
        return r.json()["result"][-1]["message"]["message_id"]

def send_poll(question : str, options, reply_to_message_id:int) -> None:
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
        "correct_option_id" : 0,
        "reply_to_message_id": reply_to_message_id
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


def send_mesg(text: str) -> None:
    data = {"text": text}
    for ID in CHAT_ID:
        data["chat_id"] = ID
        try:
            for _ in range(20):
                r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data = data)
                req_result = r.json()
                if r.status_code == 200 and req_result["ok"]:
                    print("Poll send successfuly")
                    break
                else:
                    print("error while sending the poll")
        except:
            print("Error in sending file to chat_id: ", i)



def get_sent_polls():
    runs = 0
    while True:
        try:
            r = requests.post(f"https://api.telegram.org/bot{TOKEN}/getUpdates")
            if r.status_code != 200:
                continue
            elif not r.json()["ok"]:
                continue
            else:
                results = r.json()["result"]
                output_result = []
                poll_ids = []
                for index, update in enumerate(results):
                    if poll in update and update["poll"]["id"] not in poll_ids:
                        poll_ids.append(update["poll"]["id"])
                        previous_message = results[index - 1]["message"]
                        update["chat_id"] = previous_message["chat"]["id"]
                        update["message_id"] = previous_message["message_id"]
                        output_result.append(update)
                return output_result

        except Exception as e:
            print("Error occurred:\n", e)
            if run > 20:
                return []
            else:
                run += 1
def close_poll(chat_id, message_id):
    poll_data = json.dumps({
        "chat_id" : chat_id,
        "message_id" : message_id,
    })

    for _ in range(20):
        try:
            r = requests.post(f"https://api.telegram.org/bot{TOKEN}/stopPoll", data = poll_data)
            if r.status_code != 200:
                continue
            elif not r.json()["ok"]:
                continue
            else:
                print("Ended poll", poll_data)
                return r.json()

        except Exception as e:
            print("Error occurred:\n", e)

