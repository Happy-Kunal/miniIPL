import poll
import time
import requests
question = "testing the poll"
options = ["poll tes1", "test2"]
close_time = int(time.time()) + 120

poll.send_poll(question, options, close_time)
