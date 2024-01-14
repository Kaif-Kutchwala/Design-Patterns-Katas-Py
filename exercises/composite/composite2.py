import re

class Validator:
    def validate(self, user_data: dict[str, str]) -> tuple[bool, list[str]]:
        pass

class LengthValidator(Validator):
    def __init__(self, min: int, max: int, property: str) -> None:
        self.min = min
        self.max = max
        self.property = property

    def validate(self, user_data: dict[str, str]) -> tuple[bool, list[str]]:
        if self.property not in user_data or len(user_data[self.property]) < self.min or len(user_data[self.property]) > self.max:
            return (False, f"Property '{self.property}' must be between {self.min} and {self.max} characters long")
        return (True, [])
    
class MinLengthValidator(Validator):
    def __init__(self, min: int, property: str) -> None:
        self.min = min
        self.property = property

    def validate(self, user_data: dict[str, str]) -> tuple[bool, list[str]]:
        if self.property not in user_data or len(user_data[self.property]) < self.min:
            return (False, f"Property '{self.property}' must be at least {self.min} characters long")
        return (True, [])
    
class ContainsDigitValidator(Validator):
    def __init__(self, property: str) -> None:
        self.property = property

    def validate(self, user_data: dict[str, str]) -> tuple[bool, list[str]]:
        if self.property not in user_data or  any(c.isdigit() for c in user_data[self.property]):
            return (False, f"Property '{self.property}' must contain a digit")
        return (True, [])
    
class DoesNotContainDigitValidator(Validator):
    def __init__(self, property: str) -> None:
        self.property = property

    def validate(self, user_data: dict[str, str]) -> tuple[bool, list[str]]:
        if self.property not in user_data or  any(not c.isdigit() for c in user_data[self.property]):
            return (False, f"Property '{self.property}' must be only digits")
        return (True, [])
    
class OnlyDigitValidator(Validator):
    def __init__(self, property: str) -> None:
        self.property = property

    def validate(self, user_data: dict[str, str]) -> tuple[bool, list[str]]:
        if self.property not in user_data or  all(c.isdigit() for c in user_data[self.property]):
            return (False, f"Property '{self.property}' must contain a digit")
        return (True, [])
    
class ContainsAlphanumericValidator(Validator):
    def __init__(self, property: str) -> None:
        self.property = property

    def validate(self, user_data: dict[str, str]) -> tuple[bool, list[str]]:
        if self.property not in user_data or  any(c in "!\"£$%^&*()_+-=`¬|{}[]'#@~<>?,./]" for c in user_data[self.property]):
            return (False, f"Property '{self.property}' must contain a special character")
        return (True, [])
    
class OnlyAlphanumericOrUnderscoreValidator(Validator):
    def __init__(self, property: str) -> None:
        self.property = property

    def validate(self, user_data: dict[str, str]) -> tuple[bool, list[str]]:
        if self.property not in user_data or  all(
        c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_" for c in user_data[self.property]):
            return (False, f"Property '{self.property}' must only contain alphanumerical characters or underscores")
        return (True, [])
    
class EmailValidator(Validator):
    def validate(self, user_data: dict[str, str]) -> tuple[bool, list[str]]:
        if "email" not in user_data or not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$", user_data["email"]):
            return (False, "Property 'email' must be a valid email address")
        return (True, [])
    
class FediverseIdValidator(Validator):
    def validate(self, user_data: dict[str, str]) -> tuple[bool, list[str]]:
        if "fediverse_id" not in user_data or not re.match(r"@^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$", user_data["fediverse_id"]):
            return (False, "Property 'fediverse_id' must be a valid fediverse id")
        return (True, [])
    
class NameValidator(Validator):
    def __init__(self, property: str) -> None:
        self.property = property

    def validate(self, user_data: dict[str, str]) -> tuple[bool, list[str]]:
        if (
            self.property not in user_data
            or len(user_data[self.property]) < 2
            or not user_data[self.property][0].isupper()
            or not user_data[self.property][1:].islower()
            ):
            return(False, f"Property '{self.property}' must be a valid name")
        return (True, [])
     
class OptionValidator(Validator):
    def __init__(self, options: list[str], property: str) -> None:
        self.options = options
        self.property = property

    def validate(self, user_data: dict[str, str]) -> tuple[bool, list[str]]:
        if self.property not in user_data or user_data[self.property] not in self.options:
            options_string = "' or '".join(self.options)
            return (False, f"Property '{self.property} must be one of '{options_string}'")
        return (True, [])
    
class FieldValidator(Validator):
    def __init__(self, field: str, validators: list[Validator]) -> None:
        self.field = field
        self.validators = validators

    def validate(self, user_data) -> list[str]:
        valid = True
        errors = []
        for validator in self.validators:
            result = validator.validate(user_data)
            if not result[0]:
                valid = False
                errors.append(result[1])
        if not valid:
            line_and_indent: list[tuple[int, str]] = [(1, f"All of the following {self.field} errors must be fixed:")]
            line_and_indent.extend([(2, error) for error in errors])

            return (False, "\n".join([f"{'\t' * indent}{error}" for indent, error in line_and_indent]))
        return (True, [])        

    
if __name__ == "__main__":
    example = {}
    federation_validator = FieldValidator("federation", [
        OptionValidator(["foo", "bar"],"federation_provider"),
        LengthValidator(1, 100,"federation_provider")])
    userid_validator = FieldValidator("user_id", [LengthValidator(8, 12,"user_id")])
    password_validator = FieldValidator("password", [MinLengthValidator(8, "password"), ContainsDigitValidator("password"), ContainsAlphanumericValidator("password")])
    email_validator = EmailValidator()
    fediverseid_validator = FediverseIdValidator()
    phone_validator = FieldValidator("phone", [LengthValidator(8, 10, "phone"), DoesNotContainDigitValidator("phone")])
    username_validator = FieldValidator("username", [LengthValidator(3, 20, "username"), OnlyAlphanumericOrUnderscoreValidator("username")])
    firstname_validator = FieldValidator("firstname", [NameValidator("firstname")])
    lastname_validator = FieldValidator("lastname", [NameValidator("lastname")])
    address_validator = FieldValidator("address", [LengthValidator(1, 100, "address1"), LengthValidator(1, 100, "address2")])
    postcode_validator = FieldValidator("postcode", [LengthValidator(1, 10, "postcode")])
    local_address_validator = FieldValidator("address", [address_validator, postcode_validator])
    international_address_validator = FieldValidator("address", [LengthValidator(4, 10, "state"), LengthValidator(3, 100, "city"), LengthValidator(4, 10, "zipcode"), OnlyDigitValidator("zipcode")])

    shipping_validator = FieldValidator("shipping", [local_address_validator, international_address_validator])
    non_email_login_validator = FieldValidator("non-email login", [phone_validator, username_validator])
    user_contact_validator = FieldValidator("user contact", [email_validator, fediverseid_validator, non_email_login_validator])

    user_data_validator = FieldValidator("", [
        userid_validator,
        password_validator,
        user_contact_validator,
        firstname_validator,
        lastname_validator,
        shipping_validator])
    
    federation_valid, error = federation_validator.validate(example)
    login_valid, errors = user_data_validator.validate(example)

    if federation_valid or login_valid:
        print("Valid")
    else:
        print()
        print(errors)
            