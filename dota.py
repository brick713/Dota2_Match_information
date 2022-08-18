from exceptions import RequestsException as ex
from liquipediapy import liquipediapy
import re
import unicodedata
import datetime
import pytz

class dota():

	def __init__(self,appname):
		self.appname = appname
		self.liquipedia = liquipediapy(appname,'dota2')
		self.__image_base_url = 'https://liquipedia.net'


	def get_upcoming_and_ongoing_games(self):
		games = []
		soup,__ = self.liquipedia.parse('Liquipedia:Upcoming_and_ongoing_matches')
		matches1 = soup.find_all('div',attrs={"data-toggle-area-content": "2"})[0]
		matches = matches1.find_all('table',class_='infobox_matches_content')
		for match in matches:
			game = {}
			cells = match.find_all('td')
			try:
				if cells[0].find('span',class_='team-template-text').find('a') is not None:
					game['team1'] = cells[0].find('span',class_='team-template-text').find('a').get('title')
				else:
					game['team1'] = cells[0].find('span',class_='team-template-text').find('abbr').get_text()
				game['format'] = cells[1].find('abbr').get_text()
				if cells[2].find('span',class_='team-template-text').find('a') is not None:
					game['team2'] = cells[2].find('span',class_='team-template-text').find('a').get('title')
				else:
					game['team2'] = cells[2].find('span',class_='team-template-text').find('abbr').get_text()
				timestamp = cells[3].find('span',class_="timer-object timer-object-countdown-only")['data-timestamp']
				time = int(timestamp)
				timezone = pytz.timezone('Asia/Shanghai')
				game['start_time'] = datetime.datetime.fromtimestamp(time,timezone).strftime('%Y-%m-%d-%a %H:%M:%S')
				game['tournament_short_name'] = cells[3].find('div').get_text().rstrip()
				games.append(game)	
			except AttributeError as e:
				pass

		return games	
