from api.models.metadata.validators import UserValidators, ValidatePhoneNumbers, ValidateSkills, ValidateDates, ValidateEndDate, ValidatePassword
from datetime import date

def validate_phone_numbers(phone_list: list) -> list:
    """Valida los numeros de telefono de una lista."""

    PHONE_NUMBERS_LENGHT = ValidatePhoneNumbers.PHONE_NUMBERS_LENGHT
    ERROR_MSG = ValidatePhoneNumbers.ERROR_MSG

    for num in phone_list:
        if not len(str(num)) == PHONE_NUMBERS_LENGHT:
            raise ValueError(ERROR_MSG)
    return phone_list

def validate_skills_len(skill_list: list) -> list:
    """Valida el numero maximo de caractees de una habilidad en la lista."""

    MAX_LENGHT_SKILLS = ValidateSkills.MAX_LENGHT_SKILLS
    ERROR_MSG = ValidateSkills.ERROR_MSG

    for skill in skill_list:
        if len(skill) > MAX_LENGHT_SKILLS:
            raise ValueError(ERROR_MSG)
    return skill_list

def validate_dates(testDate: date) -> date:
    """Valida que la fecha no supera la fecha actual ni sea demasiado antigua."""

    MIN_DATE = ValidateDates.MIN_DATE
    MAX_DATE = ValidateDates.MAX_DATE
    ERROR_MSG = ValidateDates.ERROR_MSG
    
    if testDate > MAX_DATE or testDate < MIN_DATE:
        raise ValueError(ERROR_MSG)
    
    return testDate

def validate_end_date(start_date: date, end_date: date) -> date:
    """Valida que la fecha de finalizacion sea posterior a la de inicio"""

    ERROR_MSG = ValidateEndDate.ERROR_MSG

    if end_date < start_date:
        raise ValueError(ERROR_MSG)
    
    return end_date

def validate_password(password: str) -> str:
    """Valida que la contraseña cumpla los requisitos de seguridad."""

    ERROR_MSG = ValidatePassword.ERROR_MSG

    if len(password) < UserValidators.MIN_LENGHT_PASSWORD:
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