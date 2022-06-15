lArgs=['hello','hi','sad']
responses={'o hi':'yo','sadd':'img.png'}
for x in responses:
    if all(i in lArgs for i in x.split(' ')):
        print(responses[x])
