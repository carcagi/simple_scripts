import tkinter as tk
import webbrowser
from tkinter import messagebox

# Set the filename for the to-do list database
filename = "todolist.txt"

# Define a function to add a new item to the to-do list
def add_item():
    # Get the text from the input field
    new_item = entry.get()

    # Append the new item to the database file
    with open(filename, "a") as file:
        file.write(new_item + "\n")

    # Clear the input field
    entry.delete(0, tk.END)

    # Refresh the to-do list display
    display_list()

# Define a function to remove an item from the to-do list
def remove_item(item):
    # Open the database file and read its contents into a list
    with open(filename, "r") as file:
        items = file.readlines()

    # Remove the selected item from the list
    items.remove(item + "\n")

    # Write the updated list back to the database file
    with open(filename, "w") as file:
        file.writelines(items)

    # Refresh the to-do list display
    display_list()

# Define a function to display the to-do list
def display_list():
    # Clear the current contents of the list display
    listbox.delete(0, tk.END)

    # Open the database file and read its contents into a list
    with open(filename, "r") as file:
        items = file.readlines()

    # Add each item to the list display
    for item in items:
        item = item.strip()
        listbox.insert(tk.END, item)

    # Bind the click event to open the browser
    listbox.bind("<Button-1>", on_list_item_click)
    listbox.bind("<Button-3>", on_list_item_click)

def on_list_item_click(event):
    index = listbox.nearest(event.y)
    item = listbox.get(index)
    
    if event.num == 1:  # Left-click
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(index)
    elif event.num == 3:  # Right-click
        if item.startswith("http://") or item.startswith("https://"):
            response = messagebox.askyesno("Confirmation", "Are you sure you want to open this page?")
            if response:
                webbrowser.open_new(item)

# Create the main window
window = tk.Tk()
window.title("To-Do List")

# Create the input field for adding new items
entry = tk.Entry(window, width=50)
entry.pack()

# Create the button for adding new items
add_button = tk.Button(window, text="Add Item", command=add_item)
add_button.pack()

# Create the list display for showing the to-do list items
listbox = tk.Listbox(window, width=100)
listbox.pack()

# Create the button for removing selected items
remove_button = tk.Button(window, text="Remove Selected", command=lambda: remove_item(listbox.get(tk.ACTIVE)))
remove_button.pack()

# Display the initial contents of the to-do list
display_list()

# Start the main event loop
window.mainloop()
