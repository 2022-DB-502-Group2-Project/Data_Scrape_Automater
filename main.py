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
teams,stadium = scraper.getTeamInformation()
CommonUtils.save_json_excel(teams,f"{data_saves_in}/Datas/team_information")
CommonUtils.save_json_excel(stadium, f"{os.getcwd()}/../Datas/stadium_information")
