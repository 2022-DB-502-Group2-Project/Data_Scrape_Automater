import os
from Scraper.scraper import Scraper
from Scraper.Utils.common import CommonUtils

data_saves_in = f"{os.getcwd()}/Datas"
scraper = Scraper()


player, player_league_history, previous_leagues = scraper.getPlayerInformation(pagination_count=2)
# player
CommonUtils.save_json_excel(player,f"{data_saves_in}/kleague_player_information")
# league history
CommonUtils.save_json_excel(player_league_history,f"{data_saves_in}/kleague_player_league_history")
# previous league history
CommonUtils.save_json_excel(previous_leagues,f"{data_saves_in}/previous_league_history")
# team informatoin
teams = scraper.getTeamInformation()
CommonUtils.save_json_excel(teams,f"{data_saves_in}/team_information")
