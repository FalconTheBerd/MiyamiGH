import tkinter as tk
import random
import json
import os

# Character lists for each rarity
one_stars = ['Leo', 'Max', 'Nina', 'Sam']
two_stars = ['Zara', 'Kai', 'Tara', 'Finn']
three_stars = ['Akane', 'Midori', 'Luna', 'Kira']
limit_broken = ['Yoru', 'Shiro']

# Loot distribution with weights
loot = [('1 Star', 500), ('2 Star', 350), ('3 Star', 144), ('Limit Broken', 6)]
three_star_pity_loot = [('3 Star', 100)]
limit_broken_pity_loot = [('Limit Broken', 1)]

# JSON save file
save_file = "miyami_misser_save.json"

# Initialize counters and variables
pull_total = 0
obtained_loot = []  # To store character names instead of rarities
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

# Save data to JSON file
def save_data():
    data = {
        "pull_total": pull_total,
        "obtained_loot": obtained_loot,  # Stores actual characters obtained
        "three_star_pity_counter": three_star_pity_counter,
        "limit_broken_pity_counter": limit_broken_pity_counter
    }
    with open(save_file, "w") as f:
        json.dump(data, f, indent=4)

# Load data from JSON file
def load_data():
    global pull_total, obtained_loot, three_star_pity_counter, limit_broken_pity_counter
    if os.path.exists(save_file):
        with open(save_file, "r") as f:
            data = json.load(f)
            pull_total = data.get("pull_total", 0)
            obtained_loot.extend(data.get("obtained_loot", []))
            three_star_pity_counter = data.get("three_star_pity_counter", 0)
            limit_broken_pity_counter = data.get("limit_broken_pity_counter", 0)
        update_display()
    else:
        save_data()  # Create the file if it doesn't exist

# Update the display with loaded data
def update_display():
    pull_total_label.config(text=f"Total Pulls: {pull_total}")
    pull_3S_pity_label.config(text=f"3 Star Pity: {three_star_pity_counter}")
    pull_LB_pity_label.config(text=f"Limit Broken Pity: {limit_broken_pity_counter}")
    update_loot_count()

# Define the pull function
def pull():
    global three_star_pity_counter, limit_broken_pity_counter, pull_total

    if limit_broken_pity_counter >= 99:  # Guarantee a Limit Broken character
        selected_character = random.choice(limit_broken)
        result_text = f'You got {selected_character}'
        limit_broken_pity_counter = 0  # Reset the Limit Broken pity counter
    elif three_star_pity_counter >= 9:  # Guarantee a 3-star character
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
    obtained_loot.append(selected_character)  # Save character name instead of rarity
    pull_result_label.config(text=result_text)
    pull_total_label.config(text=f"Total Pulls: {pull_total}")
    pull_3S_pity_label.config(text=f"3 Star Pity: {three_star_pity_counter}")
    pull_LB_pity_label.config(text=f"Limit Broken Pity: {limit_broken_pity_counter}")
    update_loot_count()
    save_data()  # Save the data after each pull

def endProgram():
    save_data()  # Save data before exiting
    root.destroy()

def pullTen():
    for _ in range(10):
        pull()

def update_loot_count():
    # Count occurrences of each character in obtained_loot
    loot_count = {character: obtained_loot.count(character) for character in set(obtained_loot)}
    
    # Prepare the text with headers for each rarity, making headers bold
    loot_count_text = ""
    
    # Order characters by rarity and add bold headers with horizontal character lists
    if any(character in loot_count for character in limit_broken):
        loot_count_text += "Limit Broken:\n  "
        loot_count_text += ", ".join(f"{character}: {loot_count[character]}" for character in limit_broken if character in loot_count)
        loot_count_text += "\n"
        
    if any(character in loot_count for character in three_stars):
        loot_count_text += "\n3 Star:\n  "
        loot_count_text += ", ".join(f"{character}: {loot_count[character]}" for character in three_stars if character in loot_count)
        loot_count_text += "\n"
        
    if any(character in loot_count for character in two_stars):
        loot_count_text += "\n2 Star:\n  "
        loot_count_text += ", ".join(f"{character}: {loot_count[character]}" for character in two_stars if character in loot_count)
        loot_count_text += "\n"
        
    if any(character in loot_count for character in one_stars):
        loot_count_text += "\n1 Star:\n  "
        loot_count_text += ", ".join(f"{character}: {loot_count[character]}" for character in one_stars if character in loot_count)
        loot_count_text += "\n"
                
    # Display the sorted and labeled character counts
    # Set the text in loot_count_label to show bold headers
    loot_count_label.config(text=loot_count_text, font=("Helvetica", 10))
    
    # Make the headings bold using tags if supported by the widget, otherwise use fonts
    loot_count_label.config(font=("Helvetica", 10, "bold"))

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
loot_count_label = tk.Label(root, text="No characters pulled yet.")
loot_count_label.pack(pady=10)

# Display LB (Limit Broken) pull pity
pull_LB_pity_label = tk.Label(root, text=f"Limit Broken Pity: {limit_broken_pity_counter}")
pull_LB_pity_label.pack(pady=10)

# Display 3S (3 Star) pull pity
pull_3S_pity_label = tk.Label(root, text=f"3 Star Pity: {three_star_pity_counter}")
pull_3S_pity_label.pack(pady=10)

# Load data on startup
load_data()

# Run the main event loop
root.mainloop()