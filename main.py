import json
import os
from Scraper.scraper import Scraper
from Scraper.Utils.common import CommonUtils

data_saves_in = os.getcwd()

scraper = Scraper()
player, player_league_history, previous_leagues = scraper.getPlayerInformation(pagination_count=1)
# player
CommonUtils.save_json_excel(player,f"{data_saves_in}/Datas/kleague_player_information")
# league history
CommonUtils.save_json_excel(player_league_history,f"{data_saves_in}/Datas/kleague_player_league_history")
CommonUtils.save_json_excel(previous_leagues,f"{data_saves_in}/Datas/previous_league_history")
# team informatoin
teams = scraper.getTeamInformation()
CommonUtils.save_json_excel(teams,f"{data_saves_in}/Datas/team_information")

# previous_leagues = dict()
# with open(f"{data_saves_in}/Datas/team_information.json","r") as j:
#     league_history = json.load(j)
#
# for k,v in league_history.items():
#     print(k)
#     print(len(v))
#
# k1,k2 = ["연도","리그"]
# filter_duplication = sorted(set(list(zip(league_history[k1],league_history[k2]))),key=lambda x:x[0])
# print(filter_duplication)
# previous_leagues[k1] = list(map(lambda x:x[0],filter_duplication))
# previous_leagues[k2] = list(map(lambda x:x[1],filter_duplication))