# You have to enable "-condebug" as a launch option and you may have to change the path to the CS2 directory

# if you want to contact me: https://linktr.ee/Mecke_Dev

import subprocess

def install_missing_requirements():
    try:
        import time
        import tkinter as tk
        from tkinter import ttk
        from tkinter import filedialog
        from googletrans import Translator
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        from pynput.keyboard import Controller, Key
        from fuzzywuzzy import fuzz
    except ImportError as e:
        print(f"Missing module: {e.name}")
        print(f"Installing the missing module using pip...")
        subprocess.call(['pip', 'install', e.name])

# Call the function to install missing requirements
install_missing_requirements()

import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from googletrans import Translator
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
import os
from pynput.keyboard import Controller, Key
from fuzzywuzzy import fuzz

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, translator, translator_name, translated_file_path, output_text, language_var):
        super().__init__()
        self.translator = translator
        self.translator_name = translator_name
        self.translated_file_path = translated_file_path
        self.translated_lines = set()
        self.output_text = output_text
        self.language_var = language_var

        # Load already translated lines from the file
        if os.path.exists(self.translated_file_path):
            with open(self.translated_file_path, "r", encoding="utf-8") as translated_file:
                self.translated_lines.update(translated_file.read().splitlines())

    def process_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        
        cfg_file_path = cfg_file_path = os.path.join(os.path.dirname(file_path), "cfg", "translate.cfg")

        for line in reversed(lines):
            if ("[ALL] " in line or "[TEAM] " in line) and line not in self.translated_lines and "ChangeGameUIState:" not in line:
                username, message = line.split(": ", 1)
                dest_language = self.language_var.get()

                if message.startswith("tm_"):
                    message = message.replace("tm_", "")
                    to_lang = message.split(" ")[0]
                    message = message.replace(to_lang, "")

                    if to_lang in languages.keys():

                        translated_message = self.translator.translate(message, dest=to_lang)

                        with open(cfg_file_path, "w", encoding="utf-8") as file:
                            file.write(f"say {translated_message.text}")

                        translated_line = f'{username[15:]}: {translated_message.text} (from {languages[translated_message.src]} to  {languages[to_lang]})'

                    else:

                        with open(cfg_file_path, "w", encoding="utf-8") as file:
                            file.write(f"say {to_lang} is not a know language code")

                        translated_line = f'{username[15:]}: tried to translate to {to_lang})'

                    

                    # Press the "L" key
                    keyboard = Controller()
                    keyboard.press('l')
                    keyboard.release('l')

                if message.startswith("code_"):
                    to_lang = message.replace("code_", "")
                    lang = None
                    real_lang = None

                    search_value_lower = to_lang.lower()
                    for key, value in languages.items():
                        value_lower = value.lower()
                        
                        # Use fuzzy matching to check for similarity
                        similarity_ratio = fuzz.ratio(search_value_lower, value_lower)
                        if similarity_ratio >= 60:
                            lang = key
                            real_lang = languages[lang]

                    # print(lang)

                    with open(cfg_file_path, "w", encoding="utf-8") as file:
                        if lang:
                            file.write(f"say The Code for {real_lang} is {lang}. Try tm_{lang} This is a test.")
                        else:
                            file.write(f"say I did not understand {to_lang.strip()}")

                    translated_line = f"Searched Code for: {to_lang}"

                    # translated_line = f'{username[15:]}: {translated_message.text} (from {languages[translated_message.src]} to  {languages[to_lang]})'

                    # Press the "L" key
                    keyboard = Controller()
                    keyboard.press('l')
                    keyboard.release('l')

                else:
                    all_or_team = "[TEAM]" if "[TEAM]" in username else "[ALL]"
                    username = ''.join(username.split(" ")[2:])
                    username = username.replace("[DEAD]", "").replace("[TEAM]", "").replace("[ALL]", "")
                    name_lang = self.translator_name.translate(username, dest=dest_language)

                    username = f"{username} ({name_lang.text} / {languages[name_lang.src]})"
                    translated_message = self.translator.translate(message, dest=dest_language)
                    translated_line = f'{all_or_team} {username}\n\t {translated_message.text} (from {languages[translated_message.src]})\n\n'

                # Update the GUI
                self.output_text.insert(tk.END, translated_line + '\n')
                self.output_text.see(tk.END)

                # Store the translated line in the set and the file
                self.translated_lines.add(line)
                with open(self.translated_file_path, "a", encoding="utf-8") as translated_file:
                    translated_file.write(line + '\n')
                break

def start_observer(console_log_path_var, output_text, language_var):
    path = console_log_path_var.get()
    translated_file_path = 'translated_lines.txt'

    translator = Translator()
    translator_name = Translator()
    event_handler = LogFileHandler(translator, translator_name, translated_file_path, output_text, language_var)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            root.update()  # Update the GUI
            time.sleep(1)  # Adjust the sleep interval as needed
            event_handler.process_file(os.path.join(path, 'console.log'))
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def clear_log(console_log_path_var):
    path = console_log_path_var.get()
    log_file_path = os.path.join(path, 'console.log')
    with open(log_file_path, 'w', encoding='utf-8'):
        pass

# Load languages from JSON
with open("languages.json", "r") as f:
    languages = json.load(f)

# Create GUI
root = tk.Tk()
root.title("Translation Log Viewer")

# Console log path input
console_log_path_var = tk.StringVar()
console_log_path_var.set(r'C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo')

path_label = tk.Label(root, text="Console Log Path:")
path_label.pack(pady=5)

path_entry = tk.Entry(root, textvariable=console_log_path_var, width=50)
path_entry.pack(pady=5)

# Language selection
language_var = tk.StringVar()
language_var.set("en")  # Set the default language to English

language_label = tk.Label(root, text="Select Language:")
language_label.pack(pady=5)

language_menu = ttk.Combobox(root, values=list(languages.values()), textvariable=language_var, state="readonly")
language_menu.pack(pady=5)

# Output text area
output_text = tk.Text(root, wrap="word", height=20, width=80)
output_text.pack(pady=10)

# Start observer button
start_button = tk.Button(root, text="Start Observer", command=lambda: start_observer(console_log_path_var, output_text, language_var))
start_button.pack(pady=10)

# Clear log button
clear_log_button = tk.Button(root, text="Clear Log", command=lambda: clear_log(console_log_path_var))
clear_log_button.pack(pady=10)

# Run the GUI
root.mainloop()
