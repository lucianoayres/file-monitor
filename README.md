# File Monitor

File Monitor is a Python script designed to effortlessly track and document changes to files within the current directory. 

## Features
- Tracks file updates (saves)
- Monitors file deletions
- Detects new file creations

## Limitations
- Only monitors changes to files within the script's execution directory
- Does not track or log directory-related modifications
- New or existing directories and their associated files are not supported and will not be monitored.

## Usage
- Download or clone the repository
- Run the 'file_monitor.py' script:

```console
python3 file_monitor.py
```
- All modifications are logged in the `file_monitor.log` file.

Feel free to customize and extend this script to suit your specific needs!