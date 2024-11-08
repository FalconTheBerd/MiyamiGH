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
obtained_loot = []  # To store unique character names
obtained_shards = {}  # To track shards for each character
choices = []
three_star_pity_counter = 0
limit_broken_pity_counter = 0

# Track displayed characters in the sidebar to avoid duplicates
displayed_characters = set()

# Populate choices based on weights
for item, weight in loot:
    choices.extend([item] * weight)

# Save data to JSON file
def save_data():
    data = {
        "pull_total": pull_total,
        "obtained_loot": obtained_loot,
        "obtained_shards": obtained_shards,  # Save shard data
        "three_star_pity_counter": three_star_pity_counter,
        "limit_broken_pity_counter": limit_broken_pity_counter
    }
    with open(save_file, "w") as f:
        json.dump(data, f, indent=4)

# Load data from JSON file
def load_data():
    global pull_total, obtained_loot, obtained_shards, three_star_pity_counter, limit_broken_pity_counter
    if os.path.exists(save_file):
        with open(save_file, "r") as f:
            data = json.load(f)
            pull_total = data.get("pull_total", 0)
            obtained_loot.clear()
            obtained_loot.extend(data.get("obtained_loot", []))
            obtained_shards.update(data.get("obtained_shards", {}))  # Load shard data
            three_star_pity_counter = data.get("three_star_pity_counter", 0)
            limit_broken_pity_counter = data.get("limit_broken_pity_counter", 0)
        update_display()
    else:
        save_data()

# Update the display with loaded data
def update_display():
    pull_total_label.config(text=f"Total Pulls: {pull_total}")
    pull_3S_pity_label.config(text=f"3 Star Pity: {three_star_pity_counter}")
    pull_LB_pity_label.config(text=f"Limit Broken Pity: {limit_broken_pity_counter}")
    update_character_grid()

# Define the pull function
def pull():
    global three_star_pity_counter, limit_broken_pity_counter, pull_total

    # Determine character rarity and prevent duplicates
    def get_unique_or_shard(char_list):
        available_chars = [char for char in char_list if char not in obtained_loot]
        if available_chars:
            return random.choice(available_chars), False  # New character
        else:
            # Return a duplicate and add a shard
            duplicate_char = random.choice(char_list)
            obtained_shards[duplicate_char] = obtained_shards.get(duplicate_char, 0) + 1
            return f"Shards of {duplicate_char}'s Blessing", True  # Shard message

    # Check for pity pulls first
    if limit_broken_pity_counter >= 99:
        selected_character, is_shard = get_unique_or_shard(limit_broken)
        result_text = f'You got {selected_character}! ⭐⭐⭐⭐' if not is_shard else selected_character
        limit_broken_pity_counter = 0
        three_star_pity_counter += 1  # Increase 3-star pity counter after any pull
    elif three_star_pity_counter >= 9:
        selected_character, is_shard = get_unique_or_shard(three_stars)
        result_text = f'You got {selected_character}! ⭐⭐⭐' if not is_shard else selected_character
        three_star_pity_counter = 0
        limit_broken_pity_counter += 1  # Increase LB pity counter after any pull
    else:
        result = random.choice(choices)
        if result == '1 Star':
            selected_character, is_shard = get_unique_or_shard(one_stars)
            result_text = f'You got {selected_character}! ⭐' if not is_shard else selected_character
        elif result == '2 Star':
            selected_character, is_shard = get_unique_or_shard(two_stars)
            result_text = f'You got {selected_character}! ⭐⭐' if not is_shard else selected_character
        elif result == '3 Star':
            selected_character, is_shard = get_unique_or_shard(three_stars)
            result_text = f'You got {selected_character}! ⭐⭐⭐' if not is_shard else selected_character
            if not is_shard:
                three_star_pity_counter = 0  # Reset 3-star pity counter after regular 3-star pull
        elif result == 'Limit Broken':
            selected_character, is_shard = get_unique_or_shard(limit_broken)
            result_text = f'You got {selected_character}! (Limit Broken) ⭐⭐⭐⭐' if not is_shard else selected_character
            limit_broken_pity_counter = 0  # Reset LB pity counter after LB pull

    # Update pity counters after every pull
    three_star_pity_counter += 1
    limit_broken_pity_counter += 1

    # Update counters and display
    pull_total += 1
    if not is_shard and selected_character not in obtained_loot:
        obtained_loot.append(selected_character)  # Add character to list if not already present
    save_data()  # Save data after each pull to store updated `obtained_loot` and `obtained_shards`
    
    # Update display
    pull_result_label.config(text=result_text)
    pull_total_label.config(text=f"Total Pulls: {pull_total}")
    pull_3S_pity_label.config(text=f"3 Star Pity: {three_star_pity_counter}")
    pull_LB_pity_label.config(text=f"Limit Broken Pity: {limit_broken_pity_counter}")
    update_character_grid()  # Update sidebar after each pull

# Define function to pull 10 times with a single sidebar update
def pullTen():
    for _ in range(10):
        pull()
    update_character_grid()  # Refresh sidebar only once after all pulls

# Update character grid display in sidebar
def update_character_grid():
    # Only add new characters to avoid refreshing the entire sidebar
    for character in obtained_loot:
        if character not in displayed_characters:
            displayed_characters.add(character)
            index = len(displayed_characters) - 1
            row, col = divmod(index, 3)
            
            # Create character frame in the sidebar grid
            char_frame = tk.Frame(sidebar, padx=5, pady=5, relief="solid", bd=1)
            char_frame.grid(row=row, column=col, padx=5, pady=5, sticky="n")

            # Placeholder for image (can replace with actual image later)
            img_label = tk.Label(char_frame, text="Image", bg="grey", width=10, height=5)
            img_label.pack()

            # Character name
            name_label = tk.Label(char_frame, text=character)
            name_label.pack()

            # Character rarity
            rarity = "⭐" * (1 if character in one_stars else 2 if character in two_stars else 3 if character in three_stars else 4)
            rarity_label = tk.Label(char_frame, text=rarity)
            rarity_label.pack()

# Toggle sidebar visibility
def toggle_sidebar():
    if sidebar.winfo_viewable():
        sidebar.grid_remove()  # Hide sidebar
        toggle_button.config(text="Show Sidebar")
    else:
        sidebar.grid()  # Show sidebar
        toggle_button.config(text="Hide Sidebar")

# Set up the main window
root = tk.Tk()
root.title("Pull Simulator")
root.geometry("1000x600")

# Sidebar for displaying obtained characters in a 3xN grid
sidebar = tk.Frame(root, width=300, bg="lightgrey")
sidebar.grid(row=0, column=0, sticky="ns")

# Main area for buttons and pull information
main_area = tk.Frame(root)
main_area.grid(row=0, column=1, sticky="nsew")

# Configure grid weights to allow resizing
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Toggle button for sidebar
toggle_button = tk.Button(root, text="Hide Sidebar", command=toggle_sidebar)
toggle_button.grid(row=1, column=0, pady=5, sticky="ew")

# Pull result display in main area
pull_result_label = tk.Label(main_area, text="Just press the button")
pull_result_label.pack(pady=10)

# Display total pulls
pull_total_label = tk.Label(main_area, text="Total Pulls: 0")
pull_total_label.pack(pady=10)

# Pull button
pull_button = tk.Button(main_area, text="Pull", command=pull)
pull_button.pack(pady=10)

# Pull 10 button
pull_ten_button = tk.Button(main_area, text="Pull x10", command=pullTen)
pull_ten_button.pack(pady=10)

# Exit button
exit_button = tk.Button(main_area, text="Exit", command=root.quit)
exit_button.pack(pady=10)

# Display Limit Broken pity counter
pull_LB_pity_label = tk.Label(main_area, text=f"Limit Broken Pity: {limit_broken_pity_counter}")
pull_LB_pity_label.pack(pady=10)

# Display 3 Star pity counter
pull_3S_pity_label = tk.Label(main_area, text=f"3 Star Pity: {three_star_pity_counter}")
pull_3S_pity_label.pack(pady=10)

# Load saved data on startup
load_data()

# Run the main event loop
root.mainloop()