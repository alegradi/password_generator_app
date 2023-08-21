from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
from datetime import date


generated_components = {}
basic_leet_dictionary = {
    "a": "4",
    "b": "8",
    "e": "3",
    "g": "6",
    "i": "1",
    "o": "0",
    "s": "5",
    "t": "7",
    "z": "2"
}
connectors = ["+", "-", "&", "@", "|", "*"]

# Create lists from files to use as the basis of passphrase generation
with open("data/adverbs.txt", "r") as file:
    adverbs_list = file.read().splitlines()

with open("data/adjectives.txt", "r") as file:
    adjectives_list = file.read().splitlines()

with open("data/nouns.txt", "r") as file:
    nouns_list = file.read().splitlines()

with open("data/verbs.txt", "r") as file:
    verb_list = file.read().splitlines()


# Function definitions
def generate_password():

    # Read the word lists and choose random
    generated_components["adverb"] = random.choice(adverbs_list)
    generated_components["adjective"] = random.choice(adjectives_list)
    generated_components["noun"] = random.choice(nouns_list)
    generated_components["verb"] = random.choice(verb_list)
    generated_components["connectors"] = ["-"]
    modifiable_options = ["noun", "adjective", "adverb", "verb"]

    if leet_word.get() == 1:
        # Select a random word to modify
        what_to_leet = random.choice(modifiable_options)
        word_to_leet = generated_components[what_to_leet]

        # Replace matches from basic_leet_dictionary
        basic_leet_result = [basic_leet_dictionary[character] if character in basic_leet_dictionary else character for
                             character in word_to_leet.lower()]

        # Debug Info
        # print(f"word_to_leet: {word_to_leet}")
        # print(f"basic_leet_results: {basic_leet_result}")

        # Construct string from basic_leet_results
        basic_leeted_word = ""
        for char in basic_leet_result:
            basic_leeted_word += char

        # print(f"basic_leeted_word: {basic_leeted_word}")  # Debug info

        generated_components[what_to_leet] = basic_leeted_word

        # Verify changes to generated_components
        # print(generated_components)

    if capitalize_word.get() == 1:
        # Select a random word to modify
        what_to_capitalize = random.choice(modifiable_options)
        word_to_capitalize = generated_components[what_to_capitalize]
        generated_components[what_to_capitalize] = word_to_capitalize.title()

    if randomized_connectors.get() == 1:
        generated_components.update({"connectors": connectors})

        # print(generated_components)

    if add_number.get() == 1:
        # Select a random word to modify
        what_to_number_append = random.choice(modifiable_options)
        word_to_number_append = generated_components[what_to_number_append]
        generated_components[what_to_number_append] = word_to_number_append + str(random.randint(0, 9))

        # print(generated_components)

    generated_password = ""
    generated_password += generated_components['adverb']
    generated_password += random.choice(generated_components["connectors"])
    generated_password += generated_components['adjective']
    generated_password += random.choice(generated_components["connectors"])
    generated_password += generated_components['noun']
    generated_password += random.choice(generated_components["connectors"])
    generated_password += generated_components['verb']

    password_entry.delete(0, END)
    password_entry.insert(index=0, string=generated_password)
    pyperclip.copy(generated_password)


def save_entries():
    """
    Use when the "Save in text file" button is pressed.
    """
    # Get data from entry fields
    website_entry_data = website_entry.get()
    username_entry_data = username_entry.get()
    password_entry_data = password_entry.get()

    new_data = {website_entry_data: {
        "email/username": username_entry_data,
        "password": password_entry_data
    }}

    if len(website_entry_data) == 0 or len(password_entry_data) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        filename = f"{date.today()}-{website_entry_data}.json"

        with open(filename, "w") as data_file:
            # Saving updated data
            json.dump(new_data, data_file, indent=4)

        # Clear the entry fields
        website_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Generator App")
window.config(padx=30, pady=30)

canvas = Canvas(width=200, height=200)
padlock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=padlock_img)
canvas.grid(column=1, row=0, columnspan=2)

# Spice it up label
spice_it_up_label = Label(text="Spice it up:", pady=5)
spice_it_up_label.grid(column=0, row=1)

# Randomize connectors checkbox
randomized_connectors = IntVar()  # Variable to hold on to checked state, 0 is off, 1 is on.
randomize_connector_checkbutton = Checkbutton(text="Randomize connectors", variable=randomized_connectors)
randomize_connector_checkbutton.grid(column=1, row=1)

# L33t it checkbox
leet_word = IntVar()
leet_word_checkbutton = Checkbutton(text=" Basic L33t it", variable=leet_word)
leet_word_checkbutton.grid(column=2, row=1)

# Add number checkbox
add_number = IntVar()
add_number_checkbutton = Checkbutton(text="Add number", variable=add_number)
add_number_checkbutton.grid(column=3, row=1)

# Capitalize word checkbox - capitalize_word
capitalize_word = IntVar()
capitalize_word_checkbutton = Checkbutton(text="Capitalize", variable=capitalize_word)
capitalize_word_checkbutton.grid(column=1, row=2)


# Additional options label
additional_options_label = Label(text="Additional options:", pady=25)
additional_options_label.grid(column=0, row=5)

# Website label
website_label = Label(text="Website:")
website_label.grid(column=0, row=6)

# Email/Username label
username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=7)

# Password label
password_label = Label(text="Password:", pady=10)
password_label.grid(column=0, row=4)

# Website entry
website_entry = Entry(width=50)
website_entry.grid(column=1, row=6, columnspan=3)
website_entry.focus()

# Email/Username entry
username_entry = Entry(width=50)
username_entry.grid(column=1, row=7, columnspan=3)
username_entry.insert(index=0, string="ferko_ferdinand@gmail.com")

# Password entry
password_entry = Entry(width=50)
password_entry.grid(column=1, row=4, columnspan=3)

# Generate password button
gen_pass_button = Button(text="Generate Password", highlightthickness=0, command=generate_password, pady=5)
gen_pass_button.grid(column=1, row=3, columnspan=2)

# Add button
add_button = Button(text="Save in text file", width=25, highlightthickness=0, command=save_entries, pady=5)
add_button.grid(column=1, row=8, columnspan=2)

window.mainloop()
