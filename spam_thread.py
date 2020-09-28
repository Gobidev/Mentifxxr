import Main
import Mentifxxr

PIN = ""
URL = ""
VOTE = 1
AMOUNT = 50


def run():

    if not PIN and URL:
        Mentifxxr.get_pin_from_url(URL)
    elif not PIN and not URL:
        print("No presentation specified")
        return

    Main.run(PIN, VOTE, AMOUNT)


if __name__ == '__main__':
    run()
