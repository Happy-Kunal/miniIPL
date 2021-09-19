import poll
import time
question = "testing the poll"
optioins = ["poll tes1", "test2"]
close_time = int(time.time()) + 120

poll.send_poll(question, optioins, close_time)
