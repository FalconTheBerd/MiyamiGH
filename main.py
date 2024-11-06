import tkinter as tk
import random

#List of 3 stars
three_stars = ['Akane', 'Midori', 'Luna', 'Kira']



loot = [('1 Star', 500), ('2 Star', 350), ('3 Star', 144), ('Limit Broken', 6)]
three_star_pity_loot = [('3 Star', 100)]
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
    global three_star_pity_counter, limit_broken_pity_counter, pull_total
    if limit_broken_pity_counter < 99: # check if limit broken is guaranteed
        if three_star_pity_counter < 9: # check if 3 star is guaranteed
            # if neither are guaranteed. do the stuff below
            result = random.choice(choices) # pick a random choice/rarity
            if result == '3 Star': # so if the rarity is three star, it should pick a character
                # so first, make it pick a character
                selected_three_star = random.choice(three_stars)
                result_text.config(text=f'You got {selected_three_star}')
                # run it
                three_star_pity_counter = 0
                pull_3S_pity_label.config(text=f"3 Star Pity: {three_star_pity_counter}")
            else:
                three_star_pity_counter += 1
                pull_3S_pity_label.config(text=f"3 Star Pity: {three_star_pity_counter}")
        else:
            result = random.choice(three_star_pity_choices)
            three_star_pity_counter = 0
            pull_3S_pity_label.config(text=f"3 Star Pity: {three_star_pity_counter}")

    else:
        result = random.choice(limit_broken_pity_choices)
        limit_broken_pity_counter = 0
        pull_LB_pity_label.config(text=f"Limit Broken Pity: {limit_broken_pity_counter}")


    if result == 'Limit Broken':
        limit_broken_pity_counter = 0
        pull_LB_pity_label.config(text=f"Limit Broken Pity: {limit_broken_pity_counter}")
    else:
        limit_broken_pity_counter += 1 
        # remember the f thing
        pull_LB_pity_label.config(text=f"Limit Broken Pity: {limit_broken_pity_counter}")

    pull_total += 1
    obtained_loot.append(result)

    if result.lower().startswith(vowels) and result != '3 Star':
        result_text = f"You got an {result}"
    else:
        if result != '3 Star':
            result_text = f"You got a {result}"

    pull_result_label.config(text=result_text)
    pull_total_label.config(text=f"Total Pulls: {pull_total}")

    update_loot_count()

def endProgram():
    exit()
    
def pullTen():
    for i in range(10):
        pull()

def update_loot_count():
    loot_count_text = (
        f"1 Star: {obtained_loot.count('1 Star')}\n"
        f"2 Star: {obtained_loot.count('2 Star')}\n"
        f"3 Star: {obtained_loot.count('3 Star')}\n"
        f"Limit Broken: {obtained_loot.count('Limit Broken')}"
    )
    loot_count_label.config(text=loot_count_text)

# Set up the main window
root = tk.Tk()
root.title("Pull Simulator")
root.geometry("1920x1080")
#  root.attributes('-fullscreen',True)

# Display pull result
pull_result_label = tk.Label(root, text="Just press the button")
pull_result_label.pack(pady=10)


# Display total pulls
pull_total_label = tk.Label(root, text="Total Pulls: 0")
pull_total_label.pack(pady=10)

# Pull button
pull_button = tk.Button(root, text="Pull", command=pull)
pull_button.pack(pady=10)

# Pull 10 button
pull_ten_button = tk.Button(root, text="Pull x10", command=pullTen)
pull_ten_button.pack(pady=10)

pull_ten_button = tk.Button(root, text="Exit", command=endProgram)
pull_ten_button.pack(pady=10)

# Display obtained loot counts
loot_count_label = tk.Label(root, text="1 Star: 0\n2 Star: 0\n3 Star: 0\nLimit Broken: 0")
loot_count_label.pack(pady=10)

# Display LB (limit broken) pull pity
pull_LB_pity_label = tk.Label(root, text= f"Limit Broken Pity: {limit_broken_pity_counter}")
pull_LB_pity_label.pack(pady=10)

# Display 3S (3 star) pull pity
pull_3S_pity_label = tk.Label(root, text= f"3 Star Pity: {three_star_pity_counter}")
pull_3S_pity_label.pack(pady=10)

# Run the main event loop
root.mainloop()