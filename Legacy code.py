
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