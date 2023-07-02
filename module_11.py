from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def validate(self, value):
        pass


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError("Phone number must be a string")
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(value) != 10:
            raise ValueError("Phone number must be 10 digits long")


class Birthday(Field):
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError("Birthday must be a string")

        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Birthday must be in format DD.MM.YYYY")

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, new_value):
            self.validate(new_value)
            self._value = new_value

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

