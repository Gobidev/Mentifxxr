import Mentifxxr


def run(pin=None, selected_number=None, times=None):

    if pin is None:
        try:
            pin = input("Input Pin\n> ")
        except ValueError:
            print("Invalid Input")
            run()

    print()

    y = Mentifxxr.get_info(pin)
    Mentifxxr.print_info(y)
    t = Mentifxxr.get_active_question_type(y)
    q = Mentifxxr.get_active_questionid(y)

    print("Current question type is:", t)
    supported_types = ["choices", "choices_images", "winner", "ranking"]

    if t in supported_types:
        if selected_number is None:
            selected_number = int(input("choose No.\n> "))
    else:
        print("Unsupported question type")
        return

    if times is None:
        try:
            times = int(input("Times\n> "))
        except ValueError:
            print("Invalid Input")
            run()
    r = range(times)

    print("sending", times, "characters")

    for x in r:
        newid = Mentifxxr.get_new_id()
        Mentifxxr.answer(q, t, newid, y, selected_number)
        print("\r", x+1, "/", len(r), end="\r")


if __name__ == '__main__':
    run()
