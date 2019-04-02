
import pandas as pd

ConfigPath="C:\Enclave\Git projects\Text Analytics\CDAT Flask\CDAT Config.xlsx"
ConfigTbl=pd.read_excel(ConfigPath)


def compareDuration(duration):
    response="No Gap"
    ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']
    StandardDuration = int(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["Values"].values[0])
    if(duration!=StandardDuration):
        return True,response
    else:
        response=str(ConfigTbl.loc[ConfigTbl['Response'] == 'Duration of liability']["Values"].values[0])
        return False,response





