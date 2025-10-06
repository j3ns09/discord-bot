import json
from random import choice


def get_random_insult():
    with open("utils/insults_db/insultes.json", "r", encoding="UTF-8") as file:
        insults = json.load(file)
        return " ".join(choice(part) for part in insults.values())
