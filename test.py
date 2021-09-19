import poll
import time
import requests
question = "testing the final poll\n who will win #30"
options = ["CSK", "MI"]

poll.send_poll(question, options)
