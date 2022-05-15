from typing import List
def useTree(message: str, tree: List[str])->str:
    for m in range(0, len(message)):
        for t in range(0,len(tree)):
            try:
                if tree[t][m] != message[m]:
                    tree[t] = ""
            except: ""
    while "" in tree:
        tree.remove("")
    if len(tree) == 1:
        output = tree[0]
    elif len(tree) > 1:
        output = f"be more spesific. possible options:\n{', '.join(tree)}"
    elif len(tree) < 1:
        output = ""
    return output

#test:
#Commands = ["helloworld","helloyou","helli","iwuaigd"]
#message = "hello"
#print(useTree(message, Commands))

def filterStrToInt(input):
    output = ""
    for i in input:
        if i.isnumeric():
            output += i
    return int(output)