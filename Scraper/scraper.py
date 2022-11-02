import os,uuid,time
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from Scraper.Utils.common import CommonUtils
from TypedPython.Validators.ParameterValidator import ParameterValidator

ParameterValidator.config('debug')

class Scraper(object):

    # Essential URLs for parsing
    __baseURL = "https://www.kleague.com/player.do"
    __stadiumByTeam = "https://namu.wiki/w/%ED%8B%80:K%EB%A6%AC%EA%B7%B81/%EA%B2%BD%EA%B8%B0%EC%9E%A5"
    __teamInfo = "https://www.kleague.com/record/team.do"

    # Kleague type
    __leagueId = {
        'kleague1' : {
            "leagueId" : 1,
            "paginationCount" : None
        },
        'kleague2' : {
            "leagueId" : 2,
            "paginationCount" : None
        }
    }

    def __init__(self):
        #Selenium driver
        self.driver = webdriver.Chrome(f"{os.path.dirname(os.path.realpath(__file__))}/chromedriver")
        # Set explicit wait
        self.explicitwait = WebDriverWait(self.driver,30)
        # Wait 3 second for driver load
        self.driver.implicitly_wait(3)
        # Get last number of pagination
        self.__initPaginationPerGroup()
        print("Initialization Finished")

    def closeDriver(self):
        self.driver.close()

    def getUUID(self):
        return uuid.uuid4()

    @ParameterValidator(isTypeMethod=True)
    def getQueryStringParamOnBasis(self,**kwargs):
        baseparam = {
            "type" : "active"
        }
        for i,v in kwargs.items():
            baseparam[i] = v
        return baseparam

    # Initialize : get pagination number per each league
    @ParameterValidator(isTypeMethod=True)
    def __initPaginationPerGroup(self):
        for i,v in Scraper.__leagueId.items():
            querystring  = urlencode(self.getQueryStringParamOnBasis(
                leagueId=v["leagueId"]
            ))
            url = f"{Scraper.__baseURL}?{querystring}"
            self.driver.get(url)

            lastbtn = self.driver.find_element(By.CLASS_NAME,'last')
            # self.explicitwait.until(ec.element_to_be_clickable((By.CLASS_NAME,'last')))
            enabled = lastbtn.is_enabled()
            # If lastbtn is enabled
            if enabled:
                self.driver.execute_script("arguments[0].click();",lastbtn)
                # selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted
                # Use Keys.Enter instead
                # lastbtn.send_keys(Keys.ENTER)
            paginationBar = self.driver.find_element(By.CLASS_NAME,"pagination")
            getlast = paginationBar.find_elements(By.CLASS_NAME,"num")[-1]
            # If limit were given and lower or equal than last pagination count
            Scraper.__leagueId[i]["paginationCount"] = int(getlast.text)

    @ParameterValidator(isTypeMethod=True)
    def getTeamInformation(self):
        # Get in page
        self.driver.get(Scraper.__teamInfo)
        # Find btn layout
        teamlists = self.driver.find_element(By.CLASS_NAME,'stadium-btn').find_element(By.CLASS_NAME,'home')
        self.driver.execute_script("arguments[0].click()",teamlists)

        html = CommonUtils.getBS4Elements(self.driver.page_source)
        columns = list(map(lambda x:x.text,html.find('div',{'id' : 'rank-div'}).find('table').find('thead').findAll('th')))
        columns.extend(["리그","image"])
        # Set team dictionary
        teams = { i : [] for i in columns }
        # Image base URL
        img_base = "https://www.kleague.com"

        league_lists_length = len(self.driver.find_element(By.ID,'leagueId').find_elements(By.TAG_NAME,'option'))
        # Initiate Dictionary Key
        print(league_lists_length)
        for i in range(league_lists_length):
            self.driver.find_element(By.ID, 'leagueId').find_elements(By.TAG_NAME, 'option')[i].click()
            # Get html
            html = CommonUtils.getBS4Elements(self.driver.page_source)
            rows = html.find("div",{"id":"rank-div"}).find('table').find('tbody').findAll('tr')
            for r in rows:
                imgurl = f"{img_base}{r.find('img').attrs['src']}"
                datas = list(map(lambda x:x.text,r.findAll("td")))
                datas.extend([list(Scraper.__leagueId.keys())[i],imgurl])
                for k,v in zip(columns,datas):
                    teams[k].append(v)
        self.driver.close()
        return teams

    @ParameterValidator(int,isTypeMethod=True)
    def getPlayerInformation(self,pagination_count=None):
        league_key = "league_type"
        player_image_key = "player_image"
        # Save player's information
        players = dict()
        # Save league history's information
        league_history = dict()
        # Save Previous league lists
        previous_leagues = dict()
        # If league history need to initiate key
        need_init = True
        for key, val in Scraper.__leagueId.items():
            page_counter = 0

            # If parameter of pagination given validate if range is valid
            # If range is not valid set original pagination counter
            if pagination_count:
                page_counter = val["paginationCount"] if pagination_count > val["paginationCount"] else pagination_count

            for i in range(1, page_counter + 1):
                # Build Query String
                querystring = urlencode(self.getQueryStringParamOnBasis(
                    page=i,
                    leagueId=val["leagueId"]
                ))
                # Build URL with URL
                url = f"{Scraper.__baseURL}?{querystring}"
                # Request with driver
                self.driver.get(url)
                # Get player list count in page
                playerlists_in_page = len(self.driver.find_elements(By.CLASS_NAME, 'player-hover'))

                for i in range(playerlists_in_page):
                    page = self.driver.find_elements(By.CLASS_NAME, 'player-hover')[i]
                    # Click with javascript event
                    self.driver.execute_script("arguments[0].click();",page)
                    # Conver to BS4 Object : To prevent non-necessary and unpredictable wait code
                    html = CommonUtils.getBS4Elements(self.driver.page_source)
                    # Extract Image URL
                    li = html.findAll('div',{'class' : 'cont-box'})

                    '''
                    ///////////////////////////////////
                    Build Database : player information
                    ///////////////////////////////////
                    '''
                    # Get img src
                    imgContent = li[0].find('img').attrs['src']
                    # Return None if not type of img
                    imgContent = imgContent if (imgContent.endswith('png') or imgContent.endswith('jpg')) else '-'
                    # Get player information
                    playerInfoList = li[1].findAll('tr')
                    player_key = None
                    # Get loop's player name
                    for i in playerInfoList:
                        child_elements = i.findChildren()
                        row_info = []
                        for i in range(0,len(child_elements),2):
                            row_key = child_elements[i].text
                            row_value = child_elements[i + 1].text
                            # If empty key -> Pass
                            if not row_key:
                                continue
                            if not row_value:
                                row_value = '-'
                            row_info.append((row_key,row_value))

                        # # If init players capsule required
                        # var = list(filter(lambda x: x, list(map(lambda x: x.text, i.findAll('th')))))
                        # value = list(filter(lambda x: x, list(map(lambda x: x.text, i.findAll('td')))))
                        for k,v in row_info:
                            if k == "이름":
                                v = f"{v}_{self.getUUID()}"
                                player_key = v
                            if k not in players.keys():
                                players[k] = [v]
                            else:
                                players[k].append(v)
                    # Add league key
                    if league_key not in players.keys():
                        players[league_key] = [key]
                    else:
                        players[league_key].append(key)
                    # Add player image key
                    if player_image_key not in players.keys():
                        players[player_image_key] = [imgContent]
                    else:
                        players[player_image_key].append(imgContent)

                    '''
                    //////////////////////////////////////////
                    Build Database : league history of players
                    //////////////////////////////////////////
                    '''
                    # Minimize Search scope for safetiness
                    leagueHistoryScope = html.find('div', {'class': 'record'})
                    # Get league history
                    getLeagueHistory = leagueHistoryScope.findAll('h3', text="정규리그")[0].parent
                    # Get title
                    historyKey = getLeagueHistory.find('h3').text
                    # Column list of league
                    getColumnList = list(map(lambda x: x.text, getLeagueHistory.find('thead').findAll('th')))
                    if need_init:
                        league_history = {i: [] for i in getColumnList}
                        league_history["이름"] = []
                        need_init = False
                    # Get Datas of league : As row
                    getHistoryDatas = getLeagueHistory.find('tbody').findAll('tr')
                    for i in getHistoryDatas:
                        # Datas per row
                        rowDatas = list(map(lambda x: x.text, i.findAll('td')))
                        for j, v in enumerate(getColumnList):
                            # Map data to right column as list via enumeration
                            league_history[v].append(rowDatas[j])
                        league_history["이름"].append(player_key)
                    print(f"Complete process : {player_key}")
                    self.driver.back()
        '''
        ///////////////////////////////
        Build Database : league history
        ///////////////////////////////
        '''
        k1,k2 = ["연도","리그"]
        # Sort by year
        filter_duplication = sorted(set(list(zip(league_history[k1],league_history[k2]))),key=lambda x:x[0])
        previous_leagues[k1] = list(map(lambda x:x[0],filter_duplication))
        previous_leagues[k2] = list(map(lambda x:x[1],filter_duplication))

        # Close driver after processing
        self.closeDriver()
        return [players,league_history,previous_leagues]

if __name__ == "__main__":
    s = Scraper()
    s.getTeamInformation()