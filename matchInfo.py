import requests
import datetime

def schedule() -> dict:
    """Returns the schedule of all matches today or after today
    Output: {"teams" : ("Team1", "Team2"), "date" : string[dd-mm-yyyy]
            "startTime" : string[HH:MM], "matchNo" : "#<SomeNumber>"}
    """
    pass

def get_next_match() -> dict :
    """Returns the matches that going to occurre today or tomorrow
    Output: {"today" : [{"teams" : ("Team1", "Team2"), "date" : string[dd-mm-yyyy]
            "startTime" : string[HH:MM], "matchNo" : "#<SomeNumber>"}, ...],
            
            "tomorrow" : <Same As For today>
    """
    pass

