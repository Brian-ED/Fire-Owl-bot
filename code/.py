
lArgs=['sssss','hi','sad']
print()
responses={'ss':'yo','sad':'img.png'}
for x in responses:
    if all(i in lArgs for i in x.split(' ')):
        print(responses[x])
        break