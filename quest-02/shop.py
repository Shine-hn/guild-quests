"""Mira's shop. A tiny game that uses the messages in messages.json.

Run: python shop.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRICES = {"lantern": 4, "rope": 3, "map": 6, "bread": 1}
BAG_LIMIT = 3


def main():
    messages = json.loads((HERE / "messages.json").read_text(encoding="utf-8"))
    money = 10
    bag = []
    print("Welcome to Mira's shop! Type 'list', 'buy <item>', or 'quit'.")
    while True:
        print()
        command = input("> ").strip().lower()
        values = {"command": command, "item": "", "price": 0, "money": money, "limit": BAG_LIMIT}
        if command == "":
            print(messages["empty_command"].format(**values))
        elif command == "quit":
            print("Come again!")
            break
        elif command == "list":
            for name, price in PRICES.items():
                print(f"  {name}: {price} gold")
            print(f"You have {money} gold. Your bag: {', '.join(bag) or 'empty'}")
        elif command.startswith("buy "):
            item = command[4:].strip()
            values.update(item=item, price=PRICES.get(item, 0))
            if item not in PRICES:
                print(messages["unknown_item"].format(**values))
            elif item in bag:
                print(messages["already_have"].format(**values))
            elif len(bag) >= BAG_LIMIT:
                print(messages["bag_full"].format(**values))
            elif PRICES[item] > money:
                print(messages["no_money"].format(**values))
            else:
                money -= PRICES[item]
                bag.append(item)
                print(f"You bought a {item}. You have {money} gold left.")
        else:
            print(messages["unknown_command"].format(**values))


if __name__ == "__main__":
    main()
