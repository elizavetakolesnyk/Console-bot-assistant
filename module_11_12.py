from collections import UserDict


class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __str__(self):
        return f"Name: {super().__str__()}"


class Phone(Field):
    def __str__(self):
        return f"Phone: {super().__str__()}"


class Record:
    def __init__(self, name: Name, phones=None):
        self.name = name
        if phones is None:
            self.phones = []
        else:
            self.phones = phones

    def add_phone(self, phone):
        self.phones.append(phone)

    def delete_phone(self, phone: Phone):
        for ph in self.phones:
            if ph.value == phone.value:
                self.phones.remove(ph)
                break

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        for index in range(self.phones):
            if self.phones[index].value == old_phone.value:
                self.phones[index] = new_phone

    def __str__(self):
        phones = '\n'.join(str(phone) for phone in self.phones)
        return f"{self.name}\n{phones}"


class AddressBook(UserDict):
    def __setitem__(self, key: Name, value: Record):
        super().__setitem__(key, value)

    def __str__(self):
        return '\n'.join(str(record) for record in self.values()) + '\n'


address_book = AddressBook()

choice = ""
while choice != "6":
    print("1) - Add record\n2) - Remove record\n3) - Change record\n4) - Show records\n5) - Find record\n6) - Exit\n")
    choice = input(">> ")

    if choice == "1":
        while True:
            name = input("<< Enter name:\n>> ")
            if name != "":
                name_field = Name(name)
                print(name_field)
                break
            else:
                print("<< Name is required field*")

        print()

        record = Record(name_field)
        while True:
            phone = input(
                "<< Enter phone:\n(Press 'Enter' for skip or 'exit' for exit)\n>> ")
            if phone != "" and phone != "exit":
                record.add_phone(Phone(phone))
            else:
                break

        address_book[record.name.value] = record
        print("<< Record is added!")
        print(address_book[name_field.value])

    if choice == "2":
        name = input("<< Enter name of record what you want to remove:\n>> ")
        if name in address_book:
            address_book.pop(name)
            print("<< Record removed!")
        else:
            print("<< Record is not found!*")

    if choice == "3":
        name = input("<< Enter name of record what you want to find:\n>> ")
        if name in address_book:
            record = address_book[name]
            choose = ""
            while choose != "5":
                choose = input(
                    "\n1) - Change name\n2) - Change phone\n3) - Add phone\n4) - Remove phone\n5) - Exit\n>> ")

                if choose == "1":
                    name = input("<< Enter name:\n>> ")
                    if name != "" and name not in address_book:
                        address_book.pop(name)
                        name_field = Name(name)
                        record.name = name_field
                        address_book[record.name.value] = record

                        print(record)

                    else:
                        print("Empty name or name is already in address book")

                if choose == "2":
                    phone = input("<< Enter phone\n>> ")
                    for ph in record.phones:
                        if ph.value == phone:
                            new_phone = input("<< Enter new phone:\n>> ")
                            if new_phone != "":
                                ph.value = new_phone
                                print(record)
                            else:
                                print("<< Error, phone is empty!*")
                if choose == "3":
                    while True:
                        phone = input(
                            "<< Enter phone:\n('exit' for exit)\n>> ")
                        if phone != "" and phone != "exit":
                            record.add_phone(Phone(phone))
                        else:
                            break

                if choose == "4":
                    phone = input("<< Enter phone\n>> ")
                    for ph in record.phones:
                        if ph.value == phone:
                            record.phones.remove(ph)
                            print("<< Phone is removed")
                            break

        else:
            print("<< Record is not found!*")

    if choice == "4":
        print(address_book)

    if choice == "5":
        choose = input("\n1) - Find by name\n2) - Find by phone\n>> ")

        if choose == "1":
            name = input("<< Enter name of record what you want to find:\n>> ")
            if name in address_book:
                record = address_book[name]
            else:
                print("<< Record is not found!*")

        if choose == "2":
            phone = input(
                "<< Enter phone of record what you want to find\n>> ")
            for name in address_book:
                for ph in address_book[name].phones:
                    if ph.value == phone:
                        print(record)
                        break
