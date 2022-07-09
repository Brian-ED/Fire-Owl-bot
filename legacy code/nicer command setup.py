commands = userCommands[:]
if isAdmin:
    commands += adminCommands
if isOwner:
    commands += ownerCommands+sum(selectPeople.values(),[])
elif msgAuthor in selectPeople:
    commands += selectPeople[msgAuthor]
commands=list(set(i.lower() for i in commands))
