import os
import sys
import subprocess
import shutil
from fuzzywuzzy import process    


SYSTEM_DESKTOP_DIR = '/usr/share/applications/'
USER_DESKTOP_DIR = f'/home/{os.getlogin()}/.local/share/applications'
HIDDEN_PATTERN = 'NoDisplay=true'

def find_best_match(pattern, choices):
    try:
        best_matches = process.extractBests(query=pattern, choices=choices, limit=10)
        best_match = best_matches[0][0]
    except TypeError:
        print(f'Nothing matches {pattern}')
        exit(1)
    if best_match != pattern:
        answer = input(f'Did you mean {best_match}? (Y/n) ')
        if not answer in ["y", "Y", ""]:
            for i in range(len(best_matches)):
                print(f'{i} - {best_matches[i][0]}')
            print("(leave empty if nothing match)")
            answer = input("Choice: ")
            if answer == "":
                print(f'"{pattern}" not found in {SYSTEM_DESKTOP_DIR}')
                exit(1)
            else:
                best_match = best_matches[int(answer)][0]

    return best_match

def already_hidden(basename):
    user_desk_entry = os.path.join(USER_DESKTOP_DIR, basename) 
    try:
        with open(user_desk_entry) as desk_file:
            lines = desk_file.readline()
            if HIDDEN_PATTERN in lines:
                return True
    except FileNotFoundError:
        return False
    return False

def hide_dektop_entry(basename):
    src = os.path.join(SYSTEM_DESKTOP_DIR, basename) 
    dst = os.path.join(USER_DESKTOP_DIR, basename) 
    shutil.copy(src, dst)
    with open(dst, 'a') as desk_file:
        desk_file.write(f'{HIDDEN_PATTERN}')


def main():
    all_files = os.listdir(SYSTEM_DESKTOP_DIR)
    desktop_entries = [f for f in all_files if f.endswith('.desktop')]

    pattern = input("Search: ")
    to_hide = find_best_match(pattern, choices=desktop_entries)
    if already_hidden(to_hide):
        print(f'{to_hide} is already hidden.')
        exit(0)
   
    update_entries_command = ['update-desktop-database', USER_DESKTOP_DIR]
    hide_dektop_entry(to_hide)
    result = subprocess.run(
        update_entries_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    print(f'{to_hide} is now hidden!')
    

if __name__ == "__main__":
    main()
