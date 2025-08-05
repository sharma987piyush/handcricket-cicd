import random
toss=["even","odd"]
play=["batting","bowling"]
run=[1,2,3,4,5,6]
AI=random.choice(run)
print("what would you like to choose even or odd ??")
user=input("user")
umpire=random.choice(toss)
print(umpire)
if umpire==user:
    user=input("call")
else:
    virat=random.choice(play)
if user=="batting":
    player=0
    while player!=AI:
        AI=random.choice(run)
        print("your score", player)
        player=int(input("player"))
        if player<=6:
            print("bowler choose",AI)
        else:
            break
        if player==AI:
            break
elif user=="bowling":
    player=0
    while player!=AI:
        AI=random.choice(run)
        print("give your delivery", player)
        player=int(input("player"))
        if player<=6:
            print("Opponent score",AI)
        else:
            break
        if player==AI:
            break
else:
    print("you lose the toss")
if virat=="batting":
    player=0
    while player!=AI:
        AI=random.choice(run)
        print("your score", player)
        player=int(input("player"))
        if player<=6:
            print("bowler choose",AI)
        else:
            break
        if player==AI:
            break
elif virat=="bowling":
    player=0
    while player!=AI:
        AI=random.choice(run)
        print("give your delivery", player)
        player=int(input("player"))
        if player<=6:
            print("Opponent score",AI)
        else:
            break
        if player==AI:
            break
else:

    print(" why are you doing this ")
