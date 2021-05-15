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


## All in one validator for disallowing Repeating and Sequential characters
## Suggested by: Hacène Dramchini CL
## LinkedIn Profile: https://www.linkedin.com/in/hdtranslations/
# class RepeatingAndSequentialValidator:
#     def __init__(self, length=4):
#         self.length = length
#
#     def check_series(self, chunk, ref):
#         for i in range(len(chunk)-1):
#             if chunk[i] + ref != chunk[i+1]:
#                 return False
#         return True
#
#     def validate(self, password, user=None):
#         ascii_list = []
#         errors = []
#         check_val = round((((self.length-1) * self.length) / 2))
#
#         for character in password:
#             ascii_list.append(ord(character))
#             for i in range(len(ascii_list)-(self.length-1)):
#                 val = (sum(ascii_list[i+1:i+self.length])) - (ascii_list[i]*3)
#                 if val == -(check_val):
#                     if self.check_series(ascii_list[i:i+self.length], -1) == True:
#                         errors.append(ValidationError(
#                             _("The password contains consecutively decreasing characters. E.g. 4321 or dcba")
#                         ))
#                 elif val == 0:
#                     if self.check_series(ascii_list[i:i+self.length], 0) == True:
#                         errors.append(ValidationError(
#                             _("The password contains characters that are consecutively repeating. e.g 1111 or aaaa")
#                         ))
#                 elif val == (check_val):
#                     if self.check_series(ascii_list[i:i+self.length], 1) == True:
#                         errors.append(ValidationError(
#                             _("The password contains consecutively increasing characters. E.g. 1234 or abcd")
#                         ))
#         if errors:
#             raise ValidationError(list(set(errors)))
#
#     def get_help_text(self):
#         return _("Password cannot contain characters that are repeating (e.g. aaaa or 1111) or sequential (e.g. 1234 or 4321 or abcd or dcba)")
