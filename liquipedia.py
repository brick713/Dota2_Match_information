from bs4 import BeautifulSoup
from requests import Session


class Liquipedia:
    def __init__(self, app_name, game):
        self._app_name = app_name
        self._game = game

        self._headers = {"User-Agent": app_name, "Accept-Encoding": "gzip"}
        self._base_url = "https://liquipedia.net/{}/api.php".format(game)

        self._session = Session()

    def _request(self, page):
        response = self._session.get(
            self._base_url,
            headers=self._headers,
            params={"action": "parse", "format": "json", "page": page},
        )
        return self._process_response(response)

    def _process_response(self, response):
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        else:
            parse = data.get("parse", {})
            text = parse.get("text", {})
            info = text.get("*")

            if not info:
                raise Exception("No parse.text.* found")

            return info

    def _parse(self, page):
        source = self._request(page)
        return BeautifulSoup(source, features="lxml")


class Dota2(Liquipedia):
    def __init__(self, app_name):
        super().__init__(app_name, "dota2")

    def get_upcoming_and_ongoing_games(self):
        games = []

        soup = self._parse("Liquipedia:Upcoming_and_ongoing_matches")

        panel_box = soup.find("div", class_="panel-box")
        if not panel_box:
            raise Exception("No div.panel-box found")

        panel_box_children = panel_box.findChildren(recursive=False)
        if len(panel_box_children) != 2:
            raise Exception("Fail to parse div.panel-box")

        panel_content = panel_box_children[1]
        # https://liquipedia.net/dota2/Liquipedia:Upcoming_and_ongoing_matches
        # 1 - Upcoming & Ongoing Matches
        # 2 - Featured Matches Only
        # 3 - Concluded Matches
        panel = panel_content.find("div", attrs={"data-toggle-area-content": "1"})
        if not panel:
            raise Exception("No div[data-toggle-area-content=1] found")

        matches = panel.find_all("table", class_="infobox_matches_content")

        games = []

        for match in matches:
            game = {}

            cells = match.find_all("td")
            if len(cells) != 4:
                continue

            [team_left, versus, team_right, match_filler] = cells

            team_left_template = team_left.find("span", class_="team-template-text")
            # dont use title, title has `(page does not exist)` sometime
            # whatever child is `a` or `abbr`, we use the get_text directly
            game["team-left"] = team_left_template.get_text()

            versus_children = versus.findChildren(recursive=False)
            if len(versus_children) != 2:
                continue
            [score, best_of] = versus_children
            game["score"] = score.get_text()
            game["best-of"] = best_of.find("abbr").get_text()

            team_right_template = team_right.find("span", class_="team-template-text")
            # dont use title, title has `(page does not exist)` sometime
            # whatever child is `a` or `abbr`, we use the get_text directly
            game["team-right"] = team_right_template.get_text()

            match_filler_children = match_filler.findChildren(recursive=False)
            if len(match_filler_children) != 2:
                continue
            [countdown, league] = match_filler_children
            game["timestamp"] = countdown.find("span", class_="timer-object").get("data-timestamp")
            game["league"] = league.get_text().rstrip()

            games.append(game)

        return games


def main():
    dota2 = Dota2("ScoresBot/2.0 (http://www.moyu.life/; hibrick713@gmail.com)")
    games = dota2.get_upcoming_and_ongoing_games()

    for game in games:
        print(game)


if __name__ == "__main__":
    main()
