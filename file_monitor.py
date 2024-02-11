import os
import time
import logging

# Default log filename
LOG_FILENAME = "./file_monitor.log"

# Script information
APP_NAME = "FileMonitor"
APP_VERSION = "0.1"
APP_LAUNCH_MESSAGE = f"[ {APP_NAME} ] v{APP_VERSION}"
APP_LOG_INFO = f"Changes will be logged in {LOG_FILENAME}"
APP_INFO_DIVIDER = "·" * 80

# Log messages
LOG_FILE_UPDATED = "File {} was updated!"
LOG_NEW_FILE_CREATED = "New file {} was created!"
LOG_FILE_DELETED = "File {} was deleted!"
LOG_INIT_TIMESTAMP_ERROR = "Error initializing timestamps: {}"
LOG_MONITORING_ERROR = "Error monitoring changes: {}"

# Script status messages
START_MESSAGE = "Monitoring started."
INTERRUPT_MESSAGE = "Monitoring interrupted."

# Log format
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

class FileMonitor:
    def __init__(self, directory, exclude_list=None):
        self.directory = directory
        self.file_timestamps = {}
        self.exclude_list = exclude_list or []

        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format=LOG_FORMAT,
            filename=LOG_FILENAME
        )

        logging.info(START_MESSAGE)

    def initialize_timestamps(self):
        try:
            for filename in os.listdir(self.directory):
                file_path = os.path.join(self.directory, filename)
                self.file_timestamps[file_path] = os.path.getmtime(file_path)
        except Exception as e:
            logging.error(LOG_INIT_TIMESTAMP_ERROR.format(e))

    def monitor_changes(self):
        try:
            while True:
                self.check_existing_files()
                self.check_new_files()
                self.check_deleted_files()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info(INTERRUPT_MESSAGE)
            print(INTERRUPT_MESSAGE)
        except Exception as e:
            message = LOG_MONITORING_ERROR.format(e)
            logging.error(message)
            print(message)

    def check_existing_files(self):
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)

            if self.should_exclude(file_path):
                continue

            current_timestamp = os.path.getmtime(file_path)
            if file_path in self.file_timestamps and self.file_timestamps[file_path] != current_timestamp:
                message = LOG_FILE_UPDATED.format(file_path)
                logging.info(message)
                print(message)
                self.file_timestamps[file_path] = current_timestamp

    def check_new_files(self):
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)

            if self.should_exclude(file_path) or not os.path.isfile(file_path):
                continue

            if file_path not in self.file_timestamps:
                message = LOG_NEW_FILE_CREATED.format(file_path)
                logging.info(message)
                print(message)
                self.file_timestamps[file_path] = os.path.getmtime(file_path)

    def check_deleted_files(self):
        for file_path in list(self.file_timestamps.keys()):
            if not os.path.exists(file_path):
                message = LOG_FILE_DELETED.format(file_path)
                logging.info(message)
                print(message)
                del self.file_timestamps[file_path]

    def should_exclude(self, item_path):
        isDirectory = os.path.isdir(item_path)
        isInTheExcludedList = item_path in self.exclude_list
        return isDirectory or isInTheExcludedList

def main():
    directory = "./"
    exclude_list = [LOG_FILENAME]

    print(APP_LAUNCH_MESSAGE)
    file_monitor = FileMonitor(directory, exclude_list)

    file_monitor.initialize_timestamps()
    
    print(APP_INFO_DIVIDER)
    print(APP_LOG_INFO)
    print("")
    file_monitor.monitor_changes()
    
if __name__ == "__main__":
    main()