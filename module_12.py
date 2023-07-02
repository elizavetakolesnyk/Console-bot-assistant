from collections import UserDict
from datetime import datetime, timedelta
import json


class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def validate(self):
        pass


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def validate(self):
        if not isinstance(self.value, str):
            raise ValueError("Phone number must be a string")
        if not self.value.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(self.value) != 10:
            raise ValueError("Phone number must be 10 digits long")


class Birthday(Field):
    def validate(self):
        if not isinstance(self.value, str):
            raise ValueError("Birthday must be a string")

        try:
            datetime.strptime(self.value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Birthday must be in format DD.MM.YYYY")

        def days_to_birthday(self):
            if self.value is None:
                return None
            today = datetime.today()
            birthday = datetime.strptime(self.value, "%d.%m.%Y")
            next_birthday = birthday.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            return (next_birthday - today).days


class Record:
    def __init__(self, name, birthday=None):
        self.name = name
        self.phones = []
        self.birthday = birthday

    def add_phone(self, phone):
        phone.validate()
        self.phones.append(phone)

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        new_phone.validate()
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    def __str__(self):
        return f"{self.name}: {', '.join(str(phone) for phone in self.phones)}"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, page_size):
        items = list(self.data.values())
        num_pages = len(items) // page_size + 1
        for i in range(num_pages):
            yield items[i * page_size: (i + 1) * page_size]

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.data, file, default=lambda obj: obj.__dict__)

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            self.data = {}
            for key, value in data.items():
                record = Record(value['name'], value['birthday'])
                record.phones = [Phone(phone) for phone in value['phones']]
                self.data[key] = record

    def search(self, query):
        results = []
        for record in self.data.values():
            if query.lower() in record.name.value.lower():
                results.append(record)
            else:
                for phone in record.phones:
                    if query.lower() in phone.value.lower():
                        results.append(record)
                        break
        return results
