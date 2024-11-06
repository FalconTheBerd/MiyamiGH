import tkinter as tk
import random

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
    if limit_broken_pity_counter < 100:
        if three_star_pity_counter < 9:
            result = random.choice(choices)
            if result == '3 Star':
                three_star_pity_counter = 0
            else:
                three_star_pity_counter += 1
        else:
            result = random.choice(three_star_pity_choices)
            three_star_pity_counter = 0
    else:
        result = random.choice(limit_broken_pity_choices)
        limit_broken_pity_counter = 0

    if result == 'Limit Broken':
        limit_broken_pity_counter = 0
    else:
        limit_broken_pity_counter += 1

    pull_total += 1
    obtained_loot.append(result)

    if result.lower().startswith(vowels):
        result_text = f"You got an {result}"
    else:
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
root.attributes('-fullscreen',True)

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

# Run the main event loop
root.mainloop()

print ("Hello world")