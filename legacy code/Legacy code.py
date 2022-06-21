
args = ['newresponse','SaD','so','reactwith:','helLo','replywith:','a','hohOHo','fun','replywith:','reactwith:']
d = {'replywith:': 'Responses', 'reactwith:': 'Reacts'}
for k in d:
    if k in args:
        indexOf=args.index(k)
        KeyStr=' '.join(args[1:indexOf]).lower()
        ValStr=' '.join(args[indexOf+1:])
        data:dict = {123:{'Reacts':{},'Responses':{}}}
        data[123][d[k]][KeyStr]=ValStr
        break





if args[0]=='ChangeSettings':
    r=''
    for i in str(msg.content.split('\n')[1:]):
        lArgs = i.split(' ')
        if lArgs[0] == 'prefix':
            if len(lArgs)<2:
                r+=f'current prefix: "{prefix}" (setting was ***not*** changed)\n'
            else:
                data[guildID]['Prefix'] = lArgs[1]
                fns.openW(datatxtPath,data)
                r+=f'Prefix changed to: "{lArgs[1]}"'
        if lArgs[:2]==['bot','channels']:
            data[guildID]['Bot channels']=args