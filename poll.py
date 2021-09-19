import json
import requests
import aiohttp
import time
import asyncio

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

async def send_poll(session : aiohttp.client.ClientSession,question : str, options, close_time : float) -> None:
    """
        This function reads the chat id from the config.json file
        and send the question and options to every chat_id
        poll is valid till close_time. close_time is a unix timem stamp
    """
    poll = {
        "question" : question,
        "options" : json.dumps(options),
        "is_anonymous" : False,
    }

    for i in CHAT_ID:
        poll["chat_id"] = i
        try:
            async with session.post(f"https://api.telegram.org/bot{TOKEN}/sendPoll", 
                    data = poll) as r:
                print(r)
        except:
            print("Error in sending file to chat_id: ", i)

async def end_poll(
        session : aiohttp.client.ClientSession,
        chat_id : str,
        message_id : int,
        end_time : float) -> None:


    poll_data = json.dumps({
        "chat_id" : chat_id,
        "message_id" : message_id,
    })
    sleep_time = end_time - time.time()
    # wait until end time
    await asyncio.sleep(sleep_time)
    try:
        async with session.post(f"https://api.telegram.org/bot{TOKEN}/sendPoll", 
                data = poll_data) as r:
            print("Ended poll", poll_data)
            x = await r.text()
            print("Ended poll is",x)
    except:
        print(f"""error in closing ending poll {poll_data}""")

