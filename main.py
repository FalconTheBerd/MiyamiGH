import random

loot = [('1 Star', 500), ('2 Star', 350), ('3 Star', 144), ('Limit Broken', 6)]
three_star_pity_loot = [('3 Star', 1)]
limit_broken_pity_loot = [('Limit Broken', 1)]
vowels = ('a', 'e', 'i', 'o', 'u')
pull_total = 0
obtained_loot = []
choices = []
three_star_pity_choices = []
limit_broken_pity_choices = []
three_star_pity_counter = 0
limit_broken_pity_counter = 0

for item, weight in loot:
    choices.extend([item] * weight)
    
for item, weight in three_star_pity_loot:
    three_star_pity_choices.extend([item] * weight)

for item, weight in limit_broken_pity_loot:
    limit_broken_pity_choices.extend([item] * weight)

def pull():
    global three_star_pity_counter, limit_broken_pity_counter
    if limit_broken_pity_counter < 100:
        if three_star_pity_counter < 10:
            pull = random.choice(choices)
            if pull == '3 Star':
                three_star_pity_counter = 0  
            else:
                three_star_pity_counter += 1  
        else:
            pull = random.choice(three_star_pity_choices)
            three_star_pity_counter = 0  

        if pull == 'Limit Broken':
            limit_broken_pity_counter = 0  
        else:
            limit_broken_pity_counter += 1  
    else:
        pull = random.choice(limit_broken_pity_choices)
        limit_broken_pity_counter = 0  

    if pull.lower().startswith(vowels):
        print("You got an " + str(pull))
    else:
        print("You got a " + str(pull))
    obtained_loot.append(pull)

while True:
    player_choice = input("What do you want to do (Help for commands): ")
    
    if player_choice.lower() == "pull":
        pull()
        pull_total += 1
    elif player_choice.lower() == "help":
        print(" Pull - Pull 1 Card \n Pull 10 - Pull 10 Cards \n Pull Total - Check your total amounts of pulls \n Obtained Loot - Check what loot you have obtained \n Show Loot Table - View the odds")
    elif player_choice.lower() == "show loot table":
        print(" A = 20% \n B = 20% \n C = 50% \n D = 10% \n E = 1%")
    elif player_choice.lower() == "pull 10" or player_choice.lower() == "10 pull":
        for i in range(10):
            pull()
            pull_total += 1
    elif player_choice.lower() == "pull total" or player_choice.lower() == "total pull":
        print("You have pulled a total of " + str(pull_total) + " times")
    elif player_choice.lower() == "obtained loot":
        print("You have " + str(obtained_loot.count('1 Star')) + " 1 Stars")
        print("You have " + str(obtained_loot.count('2 Star')) + " 2 Stars")
        print("You have " + str(obtained_loot.count('3 Star')) + " 3 Stars")
        print("You have " + str(obtained_loot.count('Limit Broken')) + " Limit Broken")
    elif player_choice.lower() == "pity":
        print("Three Star Pity: " + str(three_star_pity_counter))
        print("Limit Broken Pity: " + str(limit_broken_pity_counter))
