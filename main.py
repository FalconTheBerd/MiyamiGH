import tkinter as tk
from PIL import Image, ImageTk
import random
import json
import os

# Character lists for each rarity
one_stars = ['Leo', 'Max', 'Nina', 'Sam']
two_stars = ['Zara', 'Kai', 'Tara', 'Kori']
three_stars = ['Akane', 'Midori', 'Luna', 'Kira']
limit_broken = ['Yoru', 'Shiro', 'Miyami']

# Folder path for character images
image_folder = "images/"
save_file = "miyami_misser_save.json"

# Initialize counters and variables
pull_total = 0
obtained_loot = ['Ikari']
obtained_shards = {}
choices = []
three_star_pity_counter = 0
limit_broken_pity_counter = 0

# Dictionary to store shard labels for easy updating
shard_labels = {}
displayed_characters = set()
character_images = {}

# Weighted loot lists
loot = [('1 Star', 500), ('2 Star', 350), ('3 Star', 144), ('Limit Broken', 6)]
for item, weight in loot:
    choices.extend([item] * weight)

# Initialize Tkinter root window
root = tk.Tk()
root.title("Pull Simulator")
root.geometry("1000x800")

# Function to load images for all characters at 50x50 size for the character list
def load_images():
    for character in one_stars + two_stars + three_stars + limit_broken:
        try:
            image_path = os.path.join(image_folder, f"{character}.png")
            img = Image.open(image_path).resize((50, 50), Image.LANCZOS)
            character_images[character] = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image for {character}: {e}")

load_images()

# Save data to JSON file
def save_data():
    data = {
        "pull_total": pull_total,
        "obtained_loot": obtained_loot,
        "obtained_shards": obtained_shards,
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
            obtained_shards.update(data.get("obtained_shards", {}))
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
    update_shard_display()

# Function to update the result display after a multi-pull with larger images (160x160), arranged in 2x5 grid
def update_pull_results(pull_results):
    # Clear the previous content
    for widget in pull_result_frame.winfo_children():
        widget.destroy()

    # Configure the grid to have two rows and five columns
    for row in range(2):
        pull_result_frame.grid_rowconfigure(row, weight=1, minsize=240)
    for col in range(5):
        pull_result_frame.grid_columnconfigure(col, weight=1, minsize=160)

    # Display each character in a 2x5 grid layout
    for index, (character, is_shard) in enumerate(pull_results):
        row = index // 5
        col = index % 5

        char_frame = tk.Frame(pull_result_frame, bg="lightgrey", width=160, height=240)
        char_frame.grid(row=row, column=col, padx=5, pady=5)
        char_frame.grid_propagate(False)

        img_label = tk.Label(char_frame, bg="grey", width=160, height=160)
        img_label.pack_propagate(False)

        if character in character_images:
            # Load a separate 160x160 image for the result display
            result_image_path = os.path.join(image_folder, f"{character}.png")
            result_image = Image.open(result_image_path).resize((160, 160), Image.LANCZOS)
            result_photo = ImageTk.PhotoImage(result_image)
            img_label.config(image=result_photo)
            img_label.image = result_photo  # Keep a reference to avoid garbage collection
        else:
            img_label.config(text="Image", font=("Arial", 16))  # Placeholder if no image is available

        img_label.pack(pady=(5, 0))

        name_label = tk.Label(char_frame, text=character, font=("Arial", 16))
        name_label.pack(pady=(5, 0))

        rarity = "Shards" if is_shard else ("⭐" * (1 if character in one_stars else 2 if character in two_stars else 3 if character in three_stars else 4))
        rarity_label = tk.Label(char_frame, text=rarity, font=("Arial", 14))
        rarity_label.pack(pady=(0, 10))
        
# Pull function to generate a single result with pity mechanics
def single_pull():
    global three_star_pity_counter, limit_broken_pity_counter, pull_total

    def get_unique_or_shard(char_list):
        available_chars = [char for char in char_list if char not in obtained_loot]
        if available_chars:
            return random.choice(available_chars), False
        else:
            duplicate_char = random.choice(char_list)
            obtained_shards[duplicate_char] = obtained_shards.get(duplicate_char, 0) + 1
            return f"Shards of {duplicate_char}'s Blessing", True

    if limit_broken_pity_counter >= 99:
        selected_character, is_shard = get_unique_or_shard(limit_broken)
        limit_broken_pity_counter = 0
    elif three_star_pity_counter >= 9:
        selected_character, is_shard = get_unique_or_shard(three_stars)
        three_star_pity_counter = 0
    else:
        result = random.choice(choices)
        if result == '1 Star':
            selected_character, is_shard = get_unique_or_shard(one_stars)
        elif result == '2 Star':
            selected_character, is_shard = get_unique_or_shard(two_stars)
        elif result == '3 Star':
            selected_character, is_shard = get_unique_or_shard(three_stars)
            if not is_shard:
                three_star_pity_counter = 0
        elif result == 'Limit Broken':
            selected_character, is_shard = get_unique_or_shard(limit_broken)
            limit_broken_pity_counter = 0

    three_star_pity_counter += 1
    limit_broken_pity_counter += 1
    pull_total += 1

    # Add unique characters to obtained loot
    if not is_shard and selected_character not in obtained_loot:
        obtained_loot.append(selected_character)

    save_data()
    return selected_character, is_shard

def pull_x10():
    pull_results = [single_pull() for _ in range(10)]  # Perform 10 pulls and collect the results

    # Update the display with all 10 pull results at once
    update_pull_results(pull_results)

    # Update the counter displays
    pull_total_label.config(text=f"Total Pulls: {pull_total}")
    pull_3S_pity_label.config(text=f"3 Star Pity: {three_star_pity_counter}")
    pull_LB_pity_label.config(text=f"Limit Broken Pity: {limit_broken_pity_counter}")
    update_character_grid()
    update_shard_display()

# Pull function with pity mechanics
def pull():
    global three_star_pity_counter, limit_broken_pity_counter, pull_total
    pull_results = []  # Store results to display after Pull x10

    def get_unique_or_shard(char_list):
        available_chars = [char for char in char_list if char not in obtained_loot]
        if available_chars:
            return random.choice(available_chars), False
        else:
            duplicate_char = random.choice(char_list)
            obtained_shards[duplicate_char] = obtained_shards.get(duplicate_char, 0) + 1
            return f"Shards of {duplicate_char}'s Blessing", True

    if limit_broken_pity_counter >= 99:
        selected_character, is_shard = get_unique_or_shard(limit_broken)
        limit_broken_pity_counter = 0
    elif three_star_pity_counter >= 9:
        selected_character, is_shard = get_unique_or_shard(three_stars)
        three_star_pity_counter = 0
    else:
        result = random.choice(choices)
        if result == '1 Star':
            selected_character, is_shard = get_unique_or_shard(one_stars)
        elif result == '2 Star':
            selected_character, is_shard = get_unique_or_shard(two_stars)
        elif result == '3 Star':
            selected_character, is_shard = get_unique_or_shard(three_stars)
            if not is_shard:
                three_star_pity_counter = 0
        elif result == 'Limit Broken':
            selected_character, is_shard = get_unique_or_shard(limit_broken)
            limit_broken_pity_counter = 0

    three_star_pity_counter += 1
    limit_broken_pity_counter += 1
    pull_total += 1

    if not is_shard and selected_character not in obtained_loot:
        obtained_loot.append(selected_character)

    # Save each result for a multi-pull display
    pull_results.append((selected_character, is_shard))
    
    save_data()
    pull_total_label.config(text=f"Total Pulls: {pull_total}")
    pull_3S_pity_label.config(text=f"3 Star Pity: {three_star_pity_counter}")
    pull_LB_pity_label.config(text=f"Limit Broken Pity: {limit_broken_pity_counter}")
    update_character_grid()
    update_shard_display()
    
    # Display all results if this was a Pull x10
    update_pull_results(pull_results)

# Update character grid display in char_sidebar
def update_character_grid():
    for character in obtained_loot:
        if character not in displayed_characters:
            displayed_characters.add(character)
            index = len(displayed_characters) - 1
            row, col = divmod(index, 3)
            char_frame = tk.Frame(char_sidebar, padx=2, pady=2, relief="solid", bd=1, width=80, height=120)
            char_frame.grid(row=row, column=col, padx=5, pady=5)
            char_frame.grid_propagate(False)
            img_label = tk.Label(char_frame, bg="grey", width=50, height=50)
            if character in character_images:
                img_label.config(image=character_images[character])
                img_label.image = character_images[character]
            else:
                img_label.config(text="Image", width=8, height=4)
            img_label.pack(pady=(5, 0))
            name_label = tk.Label(char_frame, text=character, font=("Arial", 10))
            name_label.pack(pady=(5, 0))
            rarity = "⭐" * (1 if character in one_stars else 2 if character in two_stars else 3 if character in three_stars else 4)
            rarity_label = tk.Label(char_frame, text=rarity, font=("Arial", 10))
            rarity_label.pack(pady=(0, 5))

# Function to update the shard display in shard_sidebar
def update_shard_display():
    for character, shard_count in obtained_shards.items():
        if character in shard_labels:
            shard_labels[character].config(text=f"{character}: {shard_count} Shards")
        else:
            label = tk.Label(shard_sidebar, text=f"{character}: {shard_count} Shards", font=("Arial", 10), bg="lightgrey")
            label.pack(anchor="w", padx=10, pady=2)
            shard_labels[character] = label

# Configure sidebars as scrollable canvases
char_sidebar_canvas = tk.Canvas(root, width=300, bg="lightgrey")
char_sidebar_canvas.grid(row=0, column=0, rowspan=2, sticky="nsew")
char_sidebar_scrollbar = tk.Scrollbar(root, orient="vertical", command=char_sidebar_canvas.yview)
char_sidebar_scrollbar.grid(row=0, column=0, rowspan=2, sticky="nse")
char_sidebar_canvas.configure(yscrollcommand=char_sidebar_scrollbar.set)
char_sidebar = tk.Frame(char_sidebar_canvas, bg="lightgrey")
char_sidebar_canvas.create_window((0, 0), window=char_sidebar, anchor="nw")
char_sidebar.bind("<Configure>", lambda e: char_sidebar_canvas.configure(scrollregion=char_sidebar_canvas.bbox("all")))

shard_sidebar_canvas = tk.Canvas(root, width=300, bg="lightgrey")
shard_sidebar_canvas.grid(row=0, column=2, rowspan=2, sticky="nsew")
shard_sidebar_scrollbar = tk.Scrollbar(root, orient="vertical", command=shard_sidebar_canvas.yview)
shard_sidebar_scrollbar.grid(row=0, column=2, rowspan=2, sticky="nse")
shard_sidebar_canvas.configure(yscrollcommand=shard_sidebar_scrollbar.set)
shard_sidebar = tk.Frame(shard_sidebar_canvas, bg="lightgrey")
shard_sidebar_canvas.create_window((0, 0), window=shard_sidebar, anchor="nw")
shard_sidebar.bind("<Configure>", lambda e: shard_sidebar_canvas.configure(scrollregion=shard_sidebar_canvas.bbox("all")))

# Main area for pull results and buttons
main_area = tk.Frame(root)
main_area.grid(row=0, column=1, sticky="nsew")
pull_total_label = tk.Label(main_area, text="Total Pulls: 0")
pull_total_label.pack(pady=10)
pull_button = tk.Button(main_area, text="Pull", command=pull)
pull_button.pack(pady=10)
pull_ten_button = tk.Button(main_area, text="Pull x10", command=pull_x10)
pull_ten_button.pack(pady=10)
exit_button = tk.Button(main_area, text="Exit", command=root.quit)
exit_button.pack(pady=10)
pull_LB_pity_label = tk.Label(main_area, text=f"Limit Broken Pity: {limit_broken_pity_counter}")
pull_LB_pity_label.pack(pady=10)
pull_3S_pity_label = tk.Label(main_area, text=f"3 Star Pity: {three_star_pity_counter}")
pull_3S_pity_label.pack(pady=10)

# Pull result display frame with larger layout
pull_result_frame = tk.Frame(root, bg="lightgrey", width=800, height=480)  # Width to fit 5 columns, height for 2 rows
pull_result_frame.grid(row=2, column=1, pady=10, sticky="nsew")
pull_result_frame.grid_propagate(False)

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)

# Load data on startup
load_data()
update_display()
root.mainloop()