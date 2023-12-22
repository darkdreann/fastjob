from datetime import date
from api.models.metadata.validators import UserValidators, ValidatePhoneNumbers, ValidateSkills, ValidateDates, ValidateEndDate, ValidatePassword

def validate_phone_numbers(phone_list: list) -> list:
    """Valida los numeros de telefono de una lista."""

    PHONE_NUMBERS_LENGTH = ValidatePhoneNumbers.PHONE_NUMBERS_LENGTH
    ERROR_MSG = ValidatePhoneNumbers.ERROR_MSG

    for num in phone_list:
        if not len(str(num)) == PHONE_NUMBERS_LENGTH:
            raise ValueError(ERROR_MSG)
    return phone_list

def validate_skills_len(skill_list: list) -> list:
    """Valida el numero maximo de caractees de una habilidad en la lista."""

    MAX_LENGTH_SKILLS = ValidateSkills.MAX_LENGTH_SKILLS
    ERROR_MSG = ValidateSkills.ERROR_MSG

    for skill in skill_list:
        if len(skill) > MAX_LENGTH_SKILLS:
            raise ValueError(ERROR_MSG)
    return skill_list

def validate_dates(test_date: date) -> date:
    """Valida que la fecha no supera la fecha actual ni sea demasiado antigua."""

    if test_date is None: return

    MIN_DATE = ValidateDates.MIN_DATE
    MAX_DATE = ValidateDates.MAX_DATE
    ERROR_MSG = ValidateDates.ERROR_MSG
    
    if test_date > MAX_DATE or test_date < MIN_DATE:
        raise ValueError(ERROR_MSG)
    
    return test_date

def validate_end_date(start_date: date, end_date: date) -> date:
    """Valida que la fecha de finalizacion sea posterior a la de inicio"""

    if start_date is None or end_date is None: return

    ERROR_MSG = ValidateEndDate.ERROR_MSG

    if end_date < start_date:
        raise ValueError(ERROR_MSG)
    
    return end_date

def validate_password(password: str) -> str:
    """Valida que la contraseña cumpla los requisitos de seguridad."""

    ERROR_MSG = ValidatePassword.ERROR_MSG

    if len(password) < UserValidators.MIN_LENGTH_PASSWORD:
        raise ValueError(ERROR_MSG)
    if not any(letter.isupper() for letter in password):
         raise ValueError(ERROR_MSG)
    if not any(letter.islower() for letter in password):
        raise ValueError(ERROR_MSG)
    if not any(letter.isdigit() for letter in password):
        raise ValueError(ERROR_MSG)
    if not any(letter in ValidatePassword.PASSWORD_SPECIAL_CHAR for letter in password):
        raise ValueError(ERROR_MSG)
    
    return password