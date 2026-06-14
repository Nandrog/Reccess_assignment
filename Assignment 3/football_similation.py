import random


print("*+*"*20)
print("Welcome to FIFA 2026 World Cup Similation")
print("*+*"*20)
print("\n")

print("Have a chance to examine your team at a chance to victory")
print("=*="*20)
print("\n")

print ("=== FIFA World cup 2026 Winner Predictor ===")

world_cup_teams=[
    "Algeria", "Cameroon", "Côte d’Ivoire", "DR Congo", "Egypt",
    "Ghana", "Morocco", "Senegal", "South Africa", "Cape Verde",

    "Argentina", "Brazil", "Colombia", "Paraguay", "Uruguay", "Ecuador",

    "Austria", "Belgium", "Bosnia and Herzegovina", "Croatia", "Czechia",
    "England", "France", "Germany", "Netherlands", "Norway",
    "Portugal", "Scotland", "Spain", "Sweden", "Switzerland", "Türkiye",

    "Japan", "South Korea", "Iran", "Saudi Arabia", "Qatar",
    "Jordan", "Uzbekistan", "Iraq",

    "United States", "Canada", "Mexico", "Costa Rica",
    "Panama", "Curaçao", "Haiti",

    "New Zealand"
]

print("which team would You want to examine")

running = True

while running:

    response=input("(Only FIFA WORLD CUP TEAMS) Enter country you think will win(type exit to end similation): ")

    if response.lower() == "exit":
        print("Exiting similation -----")
        break

    if response=="":
        print("You entered nothing please try again.......")
        continue

    found = False


    for team in world_cup_teams:
        if team.lower()==response.lower():
            found=True
            break
    
    if not found:
        print("only teams in world cup 2026 are allowed!")
        continue
    else:
        print("similation is starting.....")
        print(f"{response} has been Grouped")

        percent_win=0
        win=0
        percent_loss=0
        percent_draw=0
        games=8
        n=0

        while True:

            qn=input(f"Has {response} played any games?")

            if qn.lower()=="":
                print("you enter nothing!")
                continue
            elif qn.lower()=="exit":
                print("exiting.....")
                break
            elif qn.lower()=="no":
                n+=1
                win+=random.random()*(n/8)*100
                percent_win+=(random.random()*(1/3)*(n/8)*100)%100
                percent_loss+=(random.random()*(1/3)*(n/8)*100)%100
                percent_draw+=100-(percent_draw+percent_loss)
                print(f"{response} has a chance of {win}% to win the world cup@!")
                print(f"{response} has chances in it's next game\n win: {percent_win}% \n draw: {percent_draw}% \n loss: {percent_loss}% ")
                break
            elif qn.lower()=="yes":
                while True:
                    num=int(input("How many games? "))
                    if num==0 or num<0:
                        print("this does not qualify")
                        continue
                    elif num>0:
                        n+=num
                        win+=random.random()*(n/8)*100
                        percent_win+=(random.random()*(1/3)*(n/8)*100) % 100
                        percent_loss+=(random.random()*(1/3)*(n/8)*100)%100
                        percent_draw+=100-(percent_draw+percent_loss)
                        print(f"{response} has a chance of {win}% to win the world cup@!")
                        print(f"{response} has chances in it's next game\n win: {percent_win}% \n draw: {percent_draw}% \n loss: {percent_loss}% ")
                        break
                    else:
                        print("quite can't understand!")
                        break
        break            


                        


            


