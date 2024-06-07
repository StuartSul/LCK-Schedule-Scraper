# Year and months to extract LCK games from
# ex. if you want to extract all LCK Summer 2024 games, 
#     set YEAR = 2024 and MONTHS = [6, 7, 8, 9]
YEAR = 2024
MONTHS = [6, 7, 8, 9]

# Whether to extract games from specified teams only
EXTRACT_ALL_TEAMS = True
TEAMS = ['T1', 'TBD'] # Only valid if EXTRACT_ALL_TEAMS = False

# Timezone info (list available at pytz.common_timezones)
# This should not be changed
TIMEZONE = 'Asia/Seoul'

# Naver E-sports schedule page format
# This should not be changed
URL_FORMAT = 'https://game.naver.com/esports/schedule/lck?date={}-{}'
