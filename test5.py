CONTACTS = {}


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found"
        except ValueError:
            return "Enter name and phone number separated by space"
        except IndexError:
            return "Enter name"
    return inner


@input_error
def add_contact(name, phone):
    CONTACTS[name] = phone
    return f"Contact {name} added"


@input_error
def change_contact(name, phone):
    CONTACTS[name] = phone
    return f"Phone number for {name} changed"


@input_error
def get_phone(name):
    return f"Phone number for {name}: {CONTACTS[name]}"


def show_all():
    if not CONTACTS:
        return "No contacts found"
    else:
        return "n".join([f"{name}: {phone}" for name, phone in CONTACTS.items()])


def main():
    while True:
        command = input("Enter command: ").lower()
        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add "):
            name, phone = command[4:].split()
            print(add_contact(name, phone))
        elif command.startswith("change "):
            name, phone = command[7:].split()
            print(change_contact(name, phone))
        elif command.startswith("phone "):
            name = command[6:]
            print(get_phone(name))
        elif command == "show all":
            print(show_all())
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
