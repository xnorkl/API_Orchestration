import pkg_resources
import time


def main():
    ''' Cron-style daemon. '''
    seconds_passed = 0
    while True:
        for entry_point in pkg_resources.iter_entry_points('daemon'):
            try:
                # Load functions registered in setup.py.
                seconds, callable = entry_point.load()()
                #print(getattr(callable, '__name__', repr(callable)))
            except Exception as e:
                print("An exeption has occured: {}".format(e))
                print("Ignoring...")
            else:
                print("else")
                if seconds_passed % seconds == 0:
                    callable()
        # Call once every hour.
        time.sleep(10)
        seconds_passed += 1
