
import tkinter as tk
from tkinter import ttk, filedialog,messagebox, scrolledtext
import random
import os

# Define a custom color scheme
bg_color = "#121212"  # Dark background color
fg_color = "#d39a02"  # Golden text color
button_color = "#121212"  # Dark for buttons
entry_bg = "#555555"  # Lighter background for entries
winner_color = "#00ff55"  # Bright green for winners
error_color = "#ff5555"  # Bright red for errors

# Custom font styles
font_style = "Cooper Black"
font_size = 12

def pick_winners(num, filepath):
    
    """
    Selects a specified number of random winners from a list of names in a file.

    Parameters:
    num (int): The number of winners to pick.
    filepath (str): The path to the file containing the list of names.

    Returns:
    tuple: A tuple containing the joined string of winners.

    """
    
    try:
        with open(filepath) as f:
            names = f.read().splitlines()
        if num > len(names):
            return "Number of winners exceeds the number of names.", 'error'
        winners = random.sample(names, num)
        winners.sort()  # This will sort the list of winners in alphabetical order
        return '\n'.join(winners), 'winner'
    except FileNotFoundError:
        return "Names file not found.", 'error'
    except ValueError:
        return "Please enter a valid number.", 'error'

def update_text(widget, message, tag=None):
    
    """
    Updates the text displayed in a Tkinter text widget with a message.

    Parameters:
    widget (tk.Text): The text widget to update.
    message (str): The message to display in the text widget.
    tag (str, optional): The tag to apply to the message for styling purposes. Defaults to None.
    """
    
    widget.delete(1.0, tk.END)
    widget.tag_configure(tag, foreground=error_color if tag == 'error' else winner_color, justify='center')
    widget.insert(tk.END, message, tag)

def on_pick_winners(entry, text, filepath):
    
    """
    Handles the event when the 'Pick Winners' button is clicked. It retrieves the number of winners from the entry widget, picks the winners, and updates the text widget.

    Parameters:
    entry (ttk.Entry): The entry widget containing the number of winners to pick.
    text (tk.Text): The text widget to update with the list of winners.
    filepath (str): The path to the file containing the list of names.

    """
    
    num = entry.get()
    if num.isdigit():
        winners, tag = pick_winners(int(num), filepath)
        update_text(text, winners, tag)
    else:
        update_text(text, "Please enter a valid number.", 'error')

def select_file(entry):
    
    """
    Opens a file dialog for the user to select a file, and updates the entry widget with the selected file path.

    Parameters:
    entry (ttk.Entry): The entry widget to update with the file path.

    """
    
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    entry.delete(0, tk.END)
    entry.insert(0, filepath)
    
def save_winners_to_file(winners):
    
    """
    Saves the list of winners to a text file on the user's desktop.

    Parameters:
    winners (str): The string containing the list of winners.
    """
    
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    file_path = os.path.join(desktop_path, 'winners_list.txt')
    with open(file_path, 'w') as file:
        file.write(winners)
    return f"Winners list saved to {file_path}"

def on_save_winners(text_widget):
    
    """
    Handles the event when the 'Save Winners' button is clicked. It retrieves the list of winners from the text widget and saves it to a file.

    Parameters:
    text_widget (tk.Text): The text widget containing the list of winners.

    """
    
    winners = text_widget.get("1.0", tk.END).strip()
    if winners:
        message = save_winners_to_file(winners)
        messagebox.showinfo("Save Successful", message)
    else:
        messagebox.showerror("Error", "No winners to save.")
        


window = tk.Tk()
window.title("Winners Picker")
window.geometry("400x600")
window.configure(background=bg_color)

style = ttk.Style()
style.configure('TButton', font=(font_style, font_size), borderwidth='4', foreground=fg_color, background=button_color)
style.configure('TEntry', font=(font_style, font_size), borderwidth='2', foreground=fg_color, background=entry_bg)
style.configure('TLabel', font=(font_style, font_size), background=bg_color, foreground=fg_color)

title_label = ttk.Label(window, text="Lottery Winners app", style='TLabel')
title_label.pack(side='top', pady=10)

file_entry = ttk.Entry(window, background=entry_bg, foreground=fg_color)
file_entry.pack(pady=10)

file_button = ttk.Button(window, text="📁 Select Names File", style='TButton', command=lambda: select_file(file_entry))
file_button.pack(pady=10)

entry_label = ttk.Label(window, text="🏆 Enter number of winners:", style='TLabel')
entry_label.pack(pady=10)

entry = ttk.Entry(window, background=entry_bg, foreground=fg_color)
entry.pack(pady=10)

button = ttk.Button(window, text="🎉 Pick Winners", style='TButton')
button.pack(pady=20)

text = scrolledtext.ScrolledText(window, height=10, width=30, bg=entry_bg, fg=fg_color)
text.pack(pady=10)
text.tag_configure('center', justify='center')

button.config(command=lambda: on_pick_winners(entry, text, file_entry.get()))

save_button = ttk.Button(window, text="💾 Save Winners", style='TButton', command=lambda: on_save_winners(text))
save_button.pack(pady=10)

window.mainloop()
