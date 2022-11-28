Data auto scraper 
===
***
- Maintainer : 윤준호(Hoplin)
- First generated : 2022 / 11 / 02
- Language : Python 3
***
## Version States

- 2022 / 11 / 28 : Stadium information scraping is now deprecated
  - Having trouble while scraping via random html tag id.
  - After changing method to `XPATH` selection, it also makes some trouble(XPATH changes randomly)
  - And we only need single time execution, and determine that it's waste of time integrate this method
***
## How to use

1. Clone project

```bash
git clone https://github.com/2022-DB-502-Group2-Project/Data_Scrape_Automater.git
```
2. Install python requirements

```bash
pip3 install -r requirements.txt
```

3. Write code

```python
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
```