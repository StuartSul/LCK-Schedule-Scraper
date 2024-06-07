# Imports

from bs4 import BeautifulSoup
from datetime import datetime
from config import *
from icalendar import Calendar, Event, vText
import json
import os
from pathlib import Path
from pytz import timezone
import requests




# Define helper methods

def new_cal(cal_description: str, cal_creator: str) -> Calendar:

    # Initialize the calendar and add required properties
    cal = Calendar()
    cal.add('prodid', f'-//{cal_description}//{cal_creator}//')
    cal.add('version', '2.0')

    return cal

def add_event(
    cal: Calendar,
    name: str,
    start_year: int,
    start_month: int,
    start_day: int,
    start_hour: int,
    start_minute: int,
    end_year: int,
    end_month: int,
    end_day: int,
    end_hour: int,
    end_minute: int,
    location: str = '',
    description: str = ''
):

    event = Event()
    event.add('summary', name)
    event.add('dtstart', datetime(
        start_year, start_month, start_day, start_hour, start_minute, 0, tzinfo=timezone(TIMEZONE))
    )
    event.add('dtend', datetime(
        end_year, end_month, end_day, end_hour, end_minute, 0, tzinfo=timezone(TIMEZONE))
    )

    if len(description) > 0:
        event.add('description', description)
    if len(location) > 0:
        event['location'] = vText(location)

    cal.add_component(event)

def save_cal(cal: Calendar, filename: str):

    with open(os.path.join(Path.cwd(), filename), 'wb') as f:
        f.write(cal.to_ical())




# Extract games, create events, and save to a calendar

if __name__ == '__main__':

    cal = new_cal('LCK Summer 2024 Match Schedules', 'stuartsul.com')

    print('===============================================')
    print('=  LCK Match Schedule Scraper by Stuart Sul   =')
    print('===============================================')
    print()
    print(f'YEAR = {YEAR}')
    print(f'MONTHS = {MONTHS}')

    if EXTRACT_ALL_TEAMS:
        print('All games')
    else:
        print(f'Games by {TEAMS}')

    for month in MONTHS:

        print()
        print(f'Game schedules for {month:02d}/{YEAR}:')

        url = URL_FORMAT.format(YEAR, month)
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        result = soup.find("script", id='__NEXT_DATA__')
        schedules = json.loads(result.text)

        for game_day in schedules['props']['initialState']['schedule']['monthSchedule']:

            for game in game_day['schedules']:

                home_team = game['homeTeam']['nameEngAcronym']
                away_team = game['awayTeam']['nameEngAcronym']
                _date = game['date'].split('월')
                month = int(_date[0])
                _date = _date[1].split('일')
                day = int(_date[0])
                _time = game['time'].split(':')
                hour = int(_time[0])
                minute = int(_time[1])

                if not EXTRACT_ALL_TEAMS and not (
                    home_team in TEAMS or away_team in TEAMS
                ):
                    continue

                print(f'  - {month:02d}/{day}/{YEAR} {hour:02d}:{minute:02d} {home_team} vs {away_team}')

                add_event(
                    cal = cal,
                    name = f'[LCK] {home_team} vs {away_team}',
                    start_year = YEAR,
                    start_month = month,
                    start_day = day,
                    start_hour = hour,
                    start_minute = minute,
                    end_year = YEAR,
                    end_month = month,
                    end_day = day,
                    end_hour = hour + 2,
                    end_minute = minute
                )

    save_cal(cal, 'schedules.ics')
