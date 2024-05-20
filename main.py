import handlers
from commands_models import Commands
from models import AddressBook

def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    print("Welcome to the assistant bot!")

    book = AddressBook()

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        # Check if command is valid
        if not Commands.is_valid(command):
            print(f"Invalid command. {command} is not found.")
            print(f"Existed commands: {Commands.get_commands()}")
            continue

        if command == Commands.HELLO.value:
            handlers.say_greeting()

        elif command == Commands.ADD.value:
            handlers.add_contact(*args, book)

        elif command == Commands.CHANGE.value:
            handlers.change_contact(*args, book)

        elif command == Commands.PHONE.value:
            name = args[0]
            phone = handlers.show_phone(name, book)

        elif command == Commands.ALL.value:
            contacts = handlers.show_all(book)

        elif command == Commands.ADD_BIRTHDAY.value:
            handlers.add_birthday(*args, book)

        elif command == Commands.SHOW_BIRTHDAY.value:
            handlers.show_birthday(*args, book)

        elif command == Commands.BIRTHDAYS.value:
            handlers.birthdays(book, *args)

        elif command in [Commands.EXIT.value, Commands.CLOSE.value]:
            print("Goodbye!")
            break

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()