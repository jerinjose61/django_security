from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ConsecutivelyRepeatingCharacterValidator:
    def __init__(self, length=4):
        self.length = length

    def validate(self, password, user=None):
        for character in password:
            if password.count(character) >= self.length:
                check_character = character * self.length

                if check_character in password:
                    raise ValidationError(
                            _("The password contains characters that are consecutively repeating. e.g 1111 or aaaa")
                            )

    def get_help_text(self):
        return _("Characters in the password cannot consecutively repeat. E.g. 1111 or aaaa")

class ConsecutivelyIncreasingIntegerValidator:
    def __init__(self, length=4):
        self.length = length

    def validate(self, password, user=None):
        for character in password:
            if character.isdigit():
                count = 0
                number = int(character)
                index = password.index(character)

                # 1234HJKuy

                try:
                    for i in range(1, self.length):
                        if password[index+i].isdigit():
                            if int(password[index+i]) == number + 1:
                                count += 1
                                number += 1

                                while count >= self.length - 1:
                                    raise ValidationError(
                                        _("The password contains consecutively increasing integers. E.g. 1234")
                                    )
                except IndexError:
                    pass

    def get_help_text(self):
        return _("Characters in the password cannot contain consecutively increasing integers. E.g. 1234")


class ConsecutivelyDecreasingIntegerValidator:
    def __init__(self, length=4):
        self.length = length

    def validate(self, password, user=None):
        for character in password:
            if character.isdigit():
                count = 0
                number = int(character)
                index = password.index(character)

                # 1234HJKuy

                try:
                    for i in range(1, self.length):
                        if password[index+i].isdigit():
                            if int(password[index+i]) == number - 1:
                                count += 1
                                number -= 1

                                while count >= self.length - 1:
                                    raise ValidationError(
                                        _("The password contains consecutively decreasing integers. E.g. 4321")
                                    )
                except IndexError:
                    pass

    def get_help_text(self):
        return _("Characters in the password cannot contain consecutively decreasing integers. E.g. 4321")

class ConsecutivelyIncreasingAlphabetValidator:
    def __init__(self, length=4):
        self.length = length

    def validate(self, password, user=None):
        for character in password:
            if character.isalpha():
                count = 0
                index = password.index(character)
                # abcd@qwerty
                try:
                    for i in range(1, self.length):
                        if password[index+i].isalpha():
                            if ord(password[index+i]) == ord(character) + 1:
                                count += 1
                                character = chr(ord(character) + 1)

                                while count >= self.length - 1:
                                    raise ValidationError(
                                        _("The password contains consecutively increasing alphabets. E.g. abcd")
                                    )
                except IndexError:
                    pass

    def get_help_text(self):
        return _("Characters in the password cannot contain consecutively increasing alphabets. E.g. abcd")

class ConsecutivelyDecreasingAlphabetValidator:
    def __init__(self, length=4):
        self.length = length

    def validate(self, password, user=None):
        for character in password:
            if character.isalpha():
                count = 0
                index = password.index(character)
                # abcd@qwerty
                try:
                    for i in range(1, self.length):
                        if password[index+i].isalpha():
                            if ord(password[index+i]) == ord(character) - 1:
                                count += 1
                                character = chr(ord(character) - 1)

                                while count >= self.length - 1:
                                    raise ValidationError(
                                        _("The password contains consecutively decreasing alphabets. E.g. dcba")
                                    )
                except IndexError:
                    pass

    def get_help_text(self):
        return _("Characters in the password cannot contain consecutively decreasing alphabets. E.g. dcba")
