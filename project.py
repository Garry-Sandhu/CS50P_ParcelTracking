from datetime import date
import sys
import inflect

p = inflect.engine()


def main():
    user_Input = input("Date of Birth: ").strip()

    today = date.today()
    birthDate = get_date(user_Input)

    delta = today - birthDate

    print(number_2_words(delta.days * 24 * 60), "minutes")


def get_date(inputDate):
    try:
        year, month, day = inputDate.split("-")
        birthDate = date(int(year), int(month), int(day))

    except ValueError:
        sys.exit("invalid Date")

    return birthDate


def number_2_words(numbers):
    return p.number_to_words(numbers, andword="").capitalize()


if __name__ == "__main__":
    main()
