a=[1,2,3,4]
print(id(a))
b=a[:]
b+=[5]

print(a)
print(id(a))
print(id(b))