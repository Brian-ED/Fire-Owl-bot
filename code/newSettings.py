loc             = 'C:/Users/brian/Persinal/discBots/'
tokenPath       = loc+'Safe/Fire-Owl-bot.yaml'
savestateDir    = loc+'data/Fire-Owl-data'
extraDir        = loc+'Fire-Owl-bot/code/extra/'
botDir          = loc+'Fire-Owl-bot/'
codeDir         = botDir+'code/'
datatxtPath     = extraDir+'data.txt'
respondstxtPath = extraDir+'responds.txt'
reactstxtPath   = extraDir+'reacts.txt'
import  functions as fns

defaultGuildSettings={'Prefix'          :'fo!',
                      'Bot channels'    :[],
                      'Replies channels':[],
                      'Reacts channels' :[],
                      'Reply delay'     :0,
                      'Replies per min' :10,
                      'Chance for reply':1,
                      'Reacts'          :fns.defaultReactsList,
                      'Responses'       :fns.defaultResponsesList}

guildID=831963301289132052

data={guildID:defaultGuildSettings}
reacts=fns.openR(reactstxtPath)
responses=fns.openR(respondstxtPath)
data[guildID]['Reacts']    = reacts
data[guildID]['Responses'] = responses
fns.openW(datatxtPath,data)