from datetime import date
from dateutil.relativedelta import relativedelta
from api.models.enums.models import WorkSchedule

#-------------------USERS---------------------------------
class UserValidators:
    MIN_LENGTH_USERNAME = 4
    MAX_LENGTH_USERNAME = 16
    MAX_LENGTH_NAME = 25 
    MAX_LENGTH_SURNAME = 25
    MAX_ITEMS_PHONE_NUMBERS = 10
    MIN_LENGTH_PASSWORD = 8
    MAX_LENGTH_PASSWORD = 30

#-------------------CANDIDATE---------------------------------
class CandidateValidators:
    MAX_ITEMS_SKILLS = 30
    MAX_ITEMS_AVAILABILITY = len(WorkSchedule)

#-------------------COMPANY---------------------------------
class CompanyValidators:
    REGEX_TIN = r"(^[A-Z][0-9]{7}[0-9A-J]$)|(^[0-9]{8}[A-Z]$)"
    MAX_LENGTH_COMPANY_NAME = 30

#-------------------LANGUAGE---------------------------------
class LanguageValidators:
    MAX_LENGTH_NAME = 35

#-------------------SECTOR---------------------------------
class SectorValidators:
    MAX_LENGTH_CATEGORY = 40
    MAX_LENGTH_SUBCATEGORY = 40

#-------------------EXPERIENCE---------------------------------
class ExperienceValidators:
    MAX_LENGTH_COMPANY_NAME = 30
    MAX_LENGTH_POSITION = 25
    MAX_LENGTH_POSITION_DESC = 200

#-------------------EDUCATION---------------------------------
class EducationValidators:
    MAX_LENGTH_QUALIFICATION = 50

#-------------------LEVEL--------------------------------------
class LevelValidators:
    MAX_LENGTH_NAME = 30
    MIN_VALUE = 0

#-------------------ADRESS--------------------------------------
class AddressValidators:
    MIN_POSTAL_CODE = 9999
    MAX_POSTAL_CODE = 100000
    POSTAL_CODE_LENGTH = 5
    MAX_LENGTH_STREET = 30
    MAX_LENGTH_CITY = 20
    MAX_LENGTH_PROVINCE = 20

#-------------------JOB--------------------------------------
class JobValidators:
    MAX_LENGTH_TITLE = 30
    MAX_LENGTH_DESC = 200
    MAX_ITEMS_SKILLS = 20
    MIN_REQUIRED_EXP = 0

#-------------------VALIDATE FUNCTIONS--------------------------------------
class ValidatePhoneNumbers:
    PHONE_NUMBERS_LENGTH = 9
    ERROR_MSG = f"El número de teléfono debe contener {PHONE_NUMBERS_LENGTH} números."

class ValidateSkills:
    MAX_LENGTH_SKILLS = 30
    ERROR_MSG = f"La longitud máxima de las habilidades es de {MAX_LENGTH_SKILLS} caracteres."

class ValidateDates:
    MIN_DATE = date.today() - relativedelta(years=80)
    MAX_DATE = date.today()
    ERROR_MSG = "La fecha no es válida."

class ValidateEndDate:
    ERROR_MSG = "La fecha de finalización debe ser posterior a la fecha de inicio."

class ValidatePassword:
    ERROR_MSG = "La contraseña debe contener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial. Como máximo 30 caracteres."
    PASSWORD_SPECIAL_CHAR = '@$!%*?&.'


