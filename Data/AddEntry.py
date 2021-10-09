from Classes.Extract import add_entry
from datetime import datetime

class AddEntry:
    """Add an entry into one of the semester files."""
    FALL_2020 = "Fall 2020.JSON"


    if __name__ == "__main__":
        id = int(input("Enter entry id: "))
        debater_id = int(input("Enter debater id: "))
        name = input("Enter debater name: ")

        add_entry()