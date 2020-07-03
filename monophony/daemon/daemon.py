import pkg_resources
import time


def main():
    ''' Cron-style daemon. '''
    seconds_passed = 0
    while True:
        for entry_point in pkg_resources.iter_entry_points('daemon'): 
            try:
                # Load functions registered in setup.py
                seconds, callable = entry_point.load()()
            except Exception as e:
                print(e)
            else:
                if seconds_passed % seconds == 0:
                    callable()
        # Call once every hour.
        time.sleep(3600)
        seconds_passed += 1
