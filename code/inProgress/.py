data={
    12: {'Self Muted':[]},
    14: {'Self Muted':[]}
}
for i in data:
    print(data[i]['Self Muted'])
data[12]['Self Muted'].append([1,2,3])
for i in data:
    print(data[i]['Self Muted'])