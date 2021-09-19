import sys
import json
import time
import datetime

import poll
import matchInfo

def main():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    if current_time == "12:00":
        schedule = matchInfo.get_next_match()
        for matchNo, matchData in schedule.items():
            options = matchData["teams"]
            poll.send_mesg(json.dumps(matchData, indent=4))
            poll.send_poll(question= f"who will win {matchNO}", options=options, reply_to_message_id=poll.get_last_update_message_id())

        time.sleep(61) # sleeping for 61 secs so that condition doesn't become true twice on same day

    live_score = matchInfo.ipl_live_score()
    if len(live_score) > 0:
        poll.send_mesg(json.dumps(live_score, indent=4))
        
        matchNo = matchInfo.get_next_match().items()[0][0]
        polls = poll.get_sent_polls()
        for poll in polls:
            if matchNo in poll["poll"]["question"]:
                poll.close_poll(chat_id=poll["chat_id"], message_id= poll["message_id"])
                
    else:
        print("Noting To Do :-(")


if __name__ == "__main__":
    while True:
        try:
            main()
            time.sleep(10)
        except KeyboardInterrupt:
            sys.exit(1)
        except Exception as e:
            print(e)




