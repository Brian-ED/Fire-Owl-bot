x = [0, 1, 1, 0]
y = [not i for i in x]
# or
z = list(map(lambda x:not x,x))
print(y)
print(z)
assert(y==z)