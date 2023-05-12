# hide-desktop-entries

Tool to hide desktop entries. Does not work for Flatpaks.

## Dependencies

`pip install fuzzywuzzy`

## Usage

Run the script and search for desktop entries in `/usr/share/applications/`. It will duplicate the matching entries in `/home/%USER/.local/share/applications` and append 'NoDisplay=true'.
