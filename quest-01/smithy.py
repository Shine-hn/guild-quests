"""The smithy reads the recipes, takes materials, readies the anvil, and lights the fire."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


class ForgeError(Exception):
    """The forge cannot finish the work."""


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def take(storehouse, material, count):
    have = storehouse[material]
    if have < count:
        raise ValueError(f"not enough {material}: need {count}, have {have}")
    storehouse[material] = have - count


def light_fire():
    try:
        with open(HERE / "coal.txt", encoding="utf-8"):
            pass
    except FileNotFoundError as err:
        raise ForgeError("the fire will not start") from err
    print("The fire is burning.")


def make(name):
    recipe = load("recipes.json")[name]
    storehouse = load("storehouse.json")
    for material, count in recipe["materials"].items():
        take(storehouse, material, count)
        print(f"Took {count} {material}.")
    anvil = load("anvil.json")
    print(f"The anvil '{anvil['name']}' is ready.")
    light_fire()
    return recipe["result"]
