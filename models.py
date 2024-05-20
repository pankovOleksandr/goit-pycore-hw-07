import re
import datetime
from collections import UserDict

class Field:
    def __init__(self, value: any):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Field):
            return False

        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

class Name(Field):
    def __init__(self, name: str):
        super().__init__(name)


class Phone(Field):
    pattern = r"[+\d]"
    country_code = "38"

    def __init__(self, phone_number: str):
        phone_number = "".join(re.findall(self.pattern, phone_number))

        if not phone_number.startswith("+"):
            phone_number = re.sub(fr"^({self.country_code})?", f"+{self.country_code}", phone_number)

        if len(phone_number) != 13:
            raise ValueError(f"Invalid phone number: {phone_number}")

        super().__init__(phone_number)

class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
            if not re.match(r"\d{2}\.\d{2}\.\d{4}", value):
                raise ValueError("Invalid date format. Use DD.MM.YYYY")
            value = datetime.datetime.strptime(value, "%d.%m.%Y")
            if value > datetime.datetime.now():
                raise ValueError("Invalid date. Birthday can't be in the future.")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str):
        if self.find_phone(phone):
            raise ValueError("Phone already exists.")
        phone = Phone(phone)
        self.phones.append(phone)
        return phone

    def remove_phone(self, phone: str):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, phone: str, new_phone: str):
        phone_to_update = self.find_phone(phone)
        if not phone_to_update:
            raise ValueError("Phone does not exist")

        self.phones[self.phones.index(phone_to_update)] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        phone = Phone(phone)
        for p in self.phones:
            if p == phone:
                return p

        return None

    def add_birthday(self, birthday: str):
         self.birthday = Birthday(birthday)

class AddressBook(UserDict):
    def add_record(self, record: Record):
        if record.name in self.data:
            raise ValueError(f"Contact {record.name} already exists.")

        self.data[record.name] = record

    def find(self, name: str):
        name = Name(name)

        if name not in self.data:
            raise ValueError(f"Contact is not exist: {name}")

        return self.data[name]

    def delete(self, name: str):
        name = Name(name)

        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, upcoming_days = 7):
        today = datetime.date.today()
        upcoming_birthdays = []
        upcoming_date = today + datetime.timedelta(upcoming_days)

        for user in self.data.values():
            if not user.birthday:
                continue
            birthday = user.birthday.value
            birthday_this_year = datetime.date(today.year, birthday.month, birthday.day)
            # 7 days including today is 6 days from today
            if today <= birthday_this_year <= upcoming_date:
                congratulation_date = birthday_this_year
                if birthday_this_year.weekday() in (5, 6):
                    congratulation_date = birthday_this_year + \
                        datetime.timedelta(days = 7 - birthday_this_year.weekday())

                upcoming_birthdays.append(
                    {
                        'name': user.name.value,
                        'congratulation_date': congratulation_date.strftime("%d.%m.%Y"),
                    }
                )


        sorted_upcoming_birthdays = sorted(upcoming_birthdays, key=lambda x: x["congratulation_date"])
        return sorted_upcoming_birthdays