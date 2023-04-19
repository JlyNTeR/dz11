import re
import datetime

class Field:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def validate(self):
        if self._value is None or self._value == '':
            return False
        return True

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        if not super().validate():
            return False
        if not re.match(r'^[a-zA-Z]+(([\',. -][a-zA-Z ])?[a-zA-Z]*)*$', self._value):
            return False
        return True


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        if not super().validate():
            return False
        if not re.match(r'^\+?[1-9]\d{1,14}$', self._value):
            return False
        return True


class Email(Field):
    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        if not super().validate():
            return False
        if not re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', self._value):
            return False
        return True


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        if not super().validate():
            return False
        if not validate_birthday(self._value):
            return False
        return True


def validate_birthday(birthday):
    try:
        datetime.datetime.strptime(birthday, '%Y-%m-%d')
        return True
    except ValueError:
        return False


class Contact:
    def __init__(self, name, email, phone=None, birthday=None):
        self.name = Name(name)
        self.email = Email(email)
        self.phone = Phone(phone) if phone else None
        self.birthday = Birthday(birthday) if birthday else None

    def __str__(self):
        phone_str = str(self.phone) if self.phone else ''
        birthday_str = str(self.birthday) if self.birthday else ''
        return f'Name: {str(self.name)}, Email: {str(self.email)}, Phone: {phone_str}, Birthday: {birthday_str}'

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.date.today()
        bday = datetime.datetime.strptime(self.birthday.value, '%Y-%m-%d').date().replace(year=today.year)
        if bday < today:
            bday = bday.replace(year=today.year + 1)
        delta = bday - today
        return delta.days

