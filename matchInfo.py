from bs4 import BeautifulSoup
import requests
import datetime

userAgent={"UserAgent":'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'}

def schedule() -> dict:
    """Returns the schedule of all matches today or after today
    Return: dict as shown below
    {
    "Match 30": {
        "teams": [
            "Chennai Super Kings ",
            " Mumbai Indians"
        ],
        "date": "19 Sept",
        "start": "19:30",
        "end": "23:30",
        "timeZone": "(IST)"
    },
    "Match 31": {
        "teams": [
            "Kolkata Knight Riders ",
            " Royal Challengers Bangalore"
        ],
        "date": "20 Sept",
        "start": "19:30",
        "end": "23:30",
        "timeZone": "(IST)"
    },
    "Match 32": {
                    ...
    },
    ...
    ...
    }
    """

    outputDict = {}
    #Getting Webpage
    url = "https://www.firstpost.com/firstcricket/cricket-schedule/series/ipl-2021.html"
    res = requests.get(url , headers=userAgent)
    soup = BeautifulSoup(res.content , features='lxml')


    #Filtering all the required information from webpage [element represents HyperText node]
    match_numbers  = tuple(map(lambda element: element.get_text().strip(), soup.findAll(class_='sc-match-txt')))
    dates = tuple(map(lambda element: element.get_text().strip(), soup.findAll(class_='schedule-txt')))
    rivals = tuple(map(lambda element: element.get_text().strip().split("vs"), soup.findAll(class_='sc-match-name')))
    timings = tuple(map(lambda element: element.get_text().replace("Time:", "").strip(), soup.findAll(class_='sc-venue-time')))
    
    #formating the gathered information into dict for output
    for (match_number, match_date, match_timing, match_rivals) in zip(match_numbers, dates, timings, rivals):
        start_timing = match_timing[:5]
        end_timing = match_timing[9:14]
        timeZone = match_timing[15:]

        outputDict[match_number] = {
                                    "teams": match_rivals,
                                    "date": match_date,
                                    "start": start_timing,
                                    "end": end_timing,
                                    "timeZone": timeZone
                                    }

    return outputDict


if __name__ == "__main__":
    import json
    print(json.dumps(schedule(), indent=4))
