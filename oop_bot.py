from collections import UserDict
import re
from typing import List, Optional

class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

class Name(Field):
    # Клас для зберігання імені контакту
    pass

class Phone(Field):
    def __init__(self, value: str):
        # Валідація номера телефону перед ініціалізацією
        if not self.validate(value):
            raise ValueError("Phone number must contain 10 digits")
        super().__init__(value)

    @staticmethod
    def validate(phone: str) -> bool:
        # Перевірка, чи містить номер телефону рівно 10 цифр
        return bool(re.match(r'^\d{10}$', phone))

class Record:
    def __init__(self, name: str):
        self.name: Name = Name(name)
        self.phones: List[Phone] = []

    def add_phone(self, phone: str) -> None:
        # Додавання нового номера телефону до запису
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        # Видалення номера телефону з запису
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        # Редагування існуючого номера телефону
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break
        else:
            raise ValueError("Phone number not found")

    def find_phone(self, phone: str) -> Optional[Phone]:
        # Пошук телефону за номером
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self) -> str:
        # Рядкове представлення запису
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        # Додавання нового запису до адресної книги
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        # Пошук запису за ім'ям
        return self.data.get(name)

    def delete(self, name: str) -> None:
        # Видалення запису за ім'ям
        if name in self.data:
            del self.data[name]



# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")