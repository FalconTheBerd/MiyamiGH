import tkinter as tk
import random

# Character lists for each rarity
one_stars = ['Leo', 'Max', 'Nina', 'Sam']
two_stars = ['Zara', 'Kai', 'Tara', 'Finn']
three_stars = ['Akane', 'Midori', 'Luna', 'Kira']
limit_broken = ['Yoru', 'Shiro']

# Loot distribution with weights
loot = [('1 Star', 500), ('2 Star', 350), ('3 Star', 144), ('Limit Broken', 6)]
three_star_pity_loot = [('3 Star', 100)]
limit_broken_pity_loot = [('Limit Broken', 1)]

# Initialize counters and variables
pull_total = 0
obtained_loot = []
choices = []
three_star_pity_choices = []
limit_broken_pity_choices = []
three_star_pity_counter = 0
limit_broken_pity_counter = 0

# Populate choices based on weights
for item, weight in loot:
    choices.extend([item] * weight)
for item, weight in three_star_pity_loot:
    three_star_pity_choices.extend([item] * weight)
for item, weight in limit_broken_pity_loot:
    limit_broken_pity_choices.extend([item] * weight)

# Define the pull function
def pull():
    global three_star_pity_counter, limit_broken_pity_counter, pull_total

    if limit_broken_pity_counter >= 99:  # Guarantee a Limit Broken character
        result = 'Limit Broken'
        selected_character = random.choice(limit_broken)
        result_text = f'You got {selected_character}'
        limit_broken_pity_counter = 0  # Reset the Limit Broken pity counter
    elif three_star_pity_counter >= 9:  # Guarantee a 3-star character
        result = '3 Star'
        selected_character = random.choice(three_stars)
        result_text = f'You got {selected_character}'
        three_star_pity_counter = 0  # Reset the 3-star pity counter
        limit_broken_pity_counter += 1  # Increment Limit Broken pity counter
    else:
        # Random pull from choices
        result = random.choice(choices)
        if result == '1 Star':
            selected_character = random.choice(one_stars)
            result_text = f'You got {selected_character}! (1 Star)'
            three_star_pity_counter += 1
            limit_broken_pity_counter += 1
        elif result == '2 Star':
            selected_character = random.choice(two_stars)
            result_text = f'You got {selected_character}! (2 Star)'
            three_star_pity_counter += 1
            limit_broken_pity_counter += 1
        elif result == '3 Star':
            selected_character = random.choice(three_stars)
            result_text = f'You got {selected_character}! (3 Star)'
            three_star_pity_counter = 0
            limit_broken_pity_counter += 1
        elif result == 'Limit Broken':
            selected_character = random.choice(limit_broken)
            result_text = f'You got {selected_character}! (Limit Broken)'
            limit_broken_pity_counter = 0  # Reset Limit Broken pity counter

    # Update counters and display
    pull_total += 1
    obtained_loot.append(result)
    pull_result_label.config(text=result_text)
    pull_total_label.config(text=f"Total Pulls: {pull_total}")
    pull_3S_pity_label.config(text=f"3 Star Pity: {three_star_pity_counter}")
    pull_LB_pity_label.config(text=f"Limit Broken Pity: {limit_broken_pity_counter}")
    update_loot_count()

def endProgram():
    exit()

def pullTen():
    for _ in range(10):
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

# Exit button
exit_button = tk.Button(root, text="Exit", command=endProgram)
exit_button.pack(pady=10)

# Display obtained loot counts
loot_count_label = tk.Label(root, text="1 Star: 0\n2 Star: 0\n3 Star: 0\nLimit Broken: 0")
loot_count_label.pack(pady=10)

# Display LB (Limit Broken) pull pity
pull_LB_pity_label = tk.Label(root, text=f"Limit Broken Pity: {limit_broken_pity_counter}")
pull_LB_pity_label.pack(pady=10)

# Display 3S (3 Star) pull pity
pull_3S_pity_label = tk.Label(root, text=f"3 Star Pity: {three_star_pity_counter}")
pull_3S_pity_label.pack(pady=10)

# Run the main event loop
root.mainloop()