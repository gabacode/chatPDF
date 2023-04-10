import os
import sys


FILES = "./files"
CACHE = f"{FILES}/.cache"


def initialize():
    if not os.path.exists(FILES):
        os.mkdir(FILES)
    if not os.path.exists(CACHE):
        os.mkdir(CACHE)


def select_file():
    os.system("clear")
    files = [file for file in os.listdir(FILES) if file.endswith(".pdf")]
    if len(files) == 0:
        return "file.pdf" if os.path.exists("file.pdf") else None
    print("📁 Select a file")
    for i, file in enumerate(files):
        print(f"{i+1}. {file}")
    print()

    try:
        possible_selections = [i for i in range(len(files) + 1)]
        selection = int(input("Enter a number, or 0 to exit: "))
        if selection == 0:
            handle_exit()
        elif selection not in possible_selections:
            select_file()
        else:
            file_path = os.path.abspath(os.path.join(FILES, files[selection - 1]))
    except ValueError:
        select_file()

    return file_path


def handle_exit():
    print("\nGoodbye!\n")
    sys.exit(1)
