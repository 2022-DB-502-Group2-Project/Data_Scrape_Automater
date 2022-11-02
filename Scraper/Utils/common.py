import bs4,json
import pandas as pd

class CommonUtils(object):
    @classmethod
    def getBS4Elements(cls,source):
        return bs4.BeautifulSoup(source,'html.parser')

    @classmethod
    def saveDictToJSON(cls,pydict,filename):
        with open(f"{filename}","w",encoding="utf-8") as w:
            # ensecure_ascii : If true vouch to be non-ascii to be escape
            # If false print in raw
            # https://docs.python.org/ko/3.7/library/json.html
            json.dump(pydict,w,indent=4,ensure_ascii=False)

    @classmethod
    def saveToEXCEL(cls,pydict,filename):
        df = pd.DataFrame(pydict)
        df.reset_index(drop=True,inplace=True)
        df.to_excel(filename)

    @classmethod
    def save_json_excel(cls,pydict,filename):
        CommonUtils.saveDictToJSON(pydict,f"{filename}.json")
        CommonUtils.saveToEXCEL(pydict,f"{filename}.xlsx")
