"""The forge of the Guild. Run: python forge.py"""
import smithy


def main():
    print("The forge is waking up...")
    item = smithy.make("hammer")
    print()
    print(f"You made a {item}!")
    print("Type this name as the answer to stage 4.")


if __name__ == "__main__":
    main()
