from dota import dota

dota_obj = dota("ScoresBot/2.0 (http://www.moyu.life/; hibrick713@gmail.com)")
games = dota_obj.get_upcoming_and_ongoing_games()
for i in games: print(i)
#print(games)
