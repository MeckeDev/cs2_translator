# You have to enable "-condebug" as a launch option and you may have to change the path to the CS2 directory
# also install this:
# pip install watchdog googletrans==4.0.0-rc1

# if you want to contact me: https://linktr.ee/Mecke_Dev

import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from googletrans import Translator

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, translator, translated_file_path):
        super().__init__()
        self.translator = translator
        self.translated_file_path = translated_file_path
        self.translated_lines = set()

        # Load already translated lines from the file
        if os.path.exists(self.translated_file_path):
            with open(self.translated_file_path, "r", encoding="utf-8") as translated_file:
                self.translated_lines.update(translated_file.read().splitlines())

    def process_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in reversed(lines):
            if ("[ALL] " in line or "[TEAM] " in line) and line not in self.translated_lines:
                username, message = line.split(": ", 1)
                translated_message = self.translator.translate(message, dest='en')
                # print(translated_message)
                print(f'{username[15:]} : {translated_message.text} (from {translated_message.src})')

                # Store the translated line in the set and the file
                self.translated_lines.add(line)
                with open(self.translated_file_path, "a", encoding="utf-8") as translated_file:
                    translated_file.write(line + '\n')
                break

if __name__ == '__main__':
    path = r'C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo'
    translated_file_path = 'translated_lines.txt'

    translator = Translator()
    event_handler = LogFileHandler(translator, translated_file_path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)  # Adjust the sleep interval as needed
            event_handler.process_file(os.path.join(path, 'console.log'))
    except KeyboardInterrupt:
        observer.stop()
    observer.join()