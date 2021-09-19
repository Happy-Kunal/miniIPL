import time
import datetime

import poll
import matchInfo

def main():
    schedule = matchInfo.get_next_match()
    for match in schedule:


