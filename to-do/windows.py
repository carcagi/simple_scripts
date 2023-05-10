import os
import sys
import subprocess
import threading
import time
import pystray
from PIL import Image

# Set the filename for the to-do list database
filename = "todolist.txt"

# Define a function to add a new item to the to-do list
def add_item(title):
    # Append the new item to the database file
    with open(filename, "a") as file:
        file.write(title + "\n")

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
    menu.clear()

    # Open the database file and read its contents into a list
    with open(filename, "r") as file:
        items = file.readlines()

    # Add each item to the list display
    for item in items:
        item = item.strip()
        menu.append(pystray.MenuItem(item, lambda item=item: remove_item(item)))

# Define a function to run the to-do list program in a separate thread
def run_todolist():
    subprocess.run([sys.executable, "todo.py"])

# Define a function to show the to-do list program window
def show_todolist_window():
    try:
        # Find the window handle for the to-do list program
        handle = win32gui.FindWindow(None, "To-Do List")

        # If the window is minimized, restore it
        if win32gui.IsIconic(handle):
            win32gui.ShowWindow(handle, win32con.SW_RESTORE)

        # Bring the window to the front and set focus to it
        win32gui.SetForegroundWindow(handle)

    except:
        # If the window handle cannot be found, run the to-do list program
        threading.Thread(target=run_todolist).start()

# Define a function to create the system tray icon
def create_system_tray():
    # Load the icon file
    icon = Image.open("icon.png")

    # Create the system tray icon and menu
    global menu
    menu = pystray.Menu(
        pystray.MenuItem("Open To-Do List", show_todolist_window),
        pystray.MenuItem("Quit", lambda: icon.stop())
    )
    icon = pystray.Icon("To-Do List", icon, menu=menu)

    # Run the icon in the system tray
    icon.run()

# Call the function to create the system tray icon
create_system_tray()
