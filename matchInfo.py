from bs4 import BeautifulSoup
import aiohttp
import datetime

userAgent={"UserAgent":'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'}

async def schedule(session : aiohttp.client.ClientSession) -> dict:
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
    async with session.get(url , headers = userAgent) as response:
        res = await response.text()
    soup = BeautifulSoup(res , features='lxml')


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


async def get_next_match(session : aiohttp.client.ClientSession) -> dict:
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
    }
    }
    #ouput dict will have 2 keys if there are two matches on the same day
    """

    outputDict = {}
    #Getting Webpage
    url = "https://www.firstpost.com/firstcricket/cricket-schedule/series/ipl-2021.html"
    async with session.get(url , headers = userAgent) as response:
        res = await response.text()
    soup = BeautifulSoup(res.content , features='lxml')


    #Filtering all the required information from webpage [element represents HyperText node]
    dates = tuple(map(lambda element: element.get_text().strip(), soup.findAll(class_='schedule-txt')[:2]))
    if dates[0] == dates[1]:
        number_of_matches_today = 2
    else:
        number_of_matches_today = 1
        dates = (dates[0], )
    
    match_numbers  = tuple(map(lambda element: element.get_text().strip(), soup.findAll(class_='sc-match-txt')[:number_of_matches_today]))
    rivals = tuple(map(lambda element: element.get_text().strip().split("vs"), soup.findAll(class_='sc-match-name')[:number_of_matches_today]))
    timings = tuple(map(lambda element: element.get_text().replace("Time:", "").strip(), soup.findAll(class_='sc-venue-time')[:number_of_matches_today]))
    
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

async def point_table(session : aiohttp.client.ClientSession):
    """Outputs The Points Table as
    [
    ['Team', 'M', 'W', 'L', 'PT', 'NRR']
    ('DC', '8', '6', '2', '12', '0.547')
    ('CSK', '7', '5', '2', '10', '1.263')
    ('RCB', '7', '5', '2', '10', '-0.171')
    ('MI', '7', '4', '3', '8', '0.062')
    ('RR', '7', '3', '4', '6', '-0.190')
    ('PBKS', '8', '3', '5', '6', '-0.368')
    ('KKR', '7', '2', '5', '4', '-0.494')
    ('SRH', '7', '1', '6', '2', '-0.623')
    ]
    """
    outputList = [["Team", "M", "W", "L", "PT", "NRR"]]
    url = "https://www.espncricinfo.com/series/_/id/8048/season/2021/indian-premier-league"

    async with session.get(url , headers = userAgent) as response:
        res = await response.text()
    soup = BeautifulSoup(res.content , features='lxml')
    points = soup.findAll(class_='pr-3')
    team = soup.findAll(class_='text-left')
    
    for i in range(5 , 45, 5):
        outputList.append((team[i//5].get_text(), points[i].get_text(),
                            points[i + 1].get_text(), points[i + 2].get_text(),
                            points[i + 3].get_text(), points[i + 4].get_text()))

    return outputList

async def ipl_live_score(session : aiohttp.client.ClientSession):
    
    live_score = {}
    
    link = 'https://m.cricbuzz.com/cricket-series/3472/indian-premier-league-2021'

    async with session.get(url , headers = userAgent) as response:
        response_sk = await response.text()
    live_score = {}
    
    if (response_sk.status_code == 200):
        sk_html = response_sk.content
        soup_sk_obtained = BeautifulSoup(sk_html,features='html.parser')

        listed_matches = soup_sk_obtained.find_all('a', class_="cb-matches-container")

        new_links = []

        for match in listed_matches:

            if match.text[0] == "L":
                new_links.append('https://m.cricbuzz.com' + match['href'])
        
        count = 1

        for link in new_links:
            async with session.get(url , headers = userAgent) as response:
                response_sk = await response.text()
            live_score = {}

            comp = ""
            rival1 = ""
            rival2 = ""
            score1 = ""
            score2 = ""
            crr = ""
            rr = ""

            if (response_sk.status_code == 200):
                sk_html = response_sk.content
                soup_sk_obtained = BeautifulSoup(sk_html,features='html.parser')

                listed_matches = soup_sk_obtained.find_all('div', class_="col-xs-9 col-lg-9 dis-inline")

                for i in soup_sk_obtained.find_all('h4', class_="cb-list-item ui-header ui-branding-header"):
                    temp = i.text
                    comp, _ = temp.split(',')

                for i in listed_matches[0].find_all('span', class_="teamscores"):
                    temp = i.text
                    rival1, score1 = temp.split('-')
                              
                for i in listed_matches[0].find_all('span', class_="miniscore-teams"):
                    temp = i.text
                    rival2, score2 = temp.split('-')
                
                j = 0
                for i in listed_matches[0].find_all('span', class_="crr"):
                    temp = i.text
                    if j ==0:
                        crr = temp
                        j += 1
                    elif j ==1:
                        rr = temp
                        j += 1
                        
                if rr[2] != ":":
                    live_score['Match ' +str(count)] = { "Now" : comp, "Team 1" : rival1[:-1], "1st innings" : score1[1:], "Team 2" : rival2[:-1], "2nd innings" : score2[1:], crr[:3] : crr[6:], rr[:2] : rr[6:]  }
                else:
                    live_score['Match ' + str(count)] = { "Now" : comp, "Team 1" : rival2[:-1], "Team 1 Score" : score2[1:], crr[:3] : crr[6:]}
                
                count += 1
    return live_score


if __name__ == "__main__":
    import json
    print(json.dumps(live_score(), indent=4))
