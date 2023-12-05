from api.models.enums.models import WorkSchedule
from datetime import date
from dateutil.relativedelta import relativedelta

#-------------------USERS---------------------------------
class UserValidators:
    MIN_LENGHT_USERNAME = 4
    MAX_LENGHT_USERNAME = 16
    MAX_LENGHT_NAME = 25 
    MAX_LENGHT_SURNAME = 25
    MAX_ITEMS_PHONE_NUMBERS = 10
    MIN_LENGHT_PASSWORD = 8
    MAX_LENGHT_PASSWORD = 30


#-------------------CANDIDATE---------------------------------
class CandidateValidators:
    MAX_ITEMS_SKILLS = 100
    MAX_ITEMS_AVAILABILITY = len(WorkSchedule)


#-------------------COMPANY---------------------------------
class CompanyValidators:
    REGEX_TIN = r"^[A-Z][0-9]{7}[0-9A-J]$|^[A-Z][0-9]{7}[0-9A-J]$|^[0-9]{8}[A-Z]$"
    MAX_LENGHT_COMPANY_NAME = 30

#-------------------LANGUAGE---------------------------------
class LanguageValidators:
    MAX_LENGHT_NAME = 20


#-------------------SECTOR---------------------------------
class SectorValidators:
    MAX_LENGHT_CATEGORY = 25
    MAX_LENGHT_SUBCATEGORY = 25

#-------------------EXPERIENCE---------------------------------
class ExperienceValidators:
    MAX_LENGHT_COMPANY_NAME = 30
    MAX_LENGHT_POSITION = 25
    MAX_LENGHT_POSITION_DESC = 200

#-------------------EDUCATION---------------------------------
class EducationValidators:
    MAX_LENGHT_QUALIFICATION = 50


#-------------------LEVEL--------------------------------------
class LevelValidators:
    MAX_LENGHT_NAME = 30
    MIN_VALUE = 0


#-------------------ADRESS--------------------------------------
class AddressValidators:
    MIN_POSTAL_CODE = 9999
    MAX_POSTAL_CODE = 100000
    MAX_LENGHT_STREET = 30
    MAX_LENGHT_CITY = 20
    MAX_LENGHT_PROVINCE = 20

#-------------------JOB--------------------------------------
class JobValidators:
    MAX_LENGHT_TITLE = 30
    MAX_LENGHT_DESC = 200
    MAX_ITEMS_SKILLS = 50
    MIN_REQUIRED_EXP = 0


#-------------------VALIDATE FUCTIONS--------------------------------------
class ValidatePhoneNumbers:
    PHONE_NUMBERS_LENGHT = 9
    ERROR_MSG = f"El número de teléfono debe contener {PHONE_NUMBERS_LENGHT} números."

class ValidateSkills:
    MAX_LENGHT_SKILLS = 20
    ERROR_MSG = f"La longitud máxima de las habilidades es de {MAX_LENGHT_SKILLS} caracteres."

class ValidateDates:
    MIN_DATE = date.today() - relativedelta(years=80)
    MAX_DATE = date.today()
    ERROR_MSG = "La fecha no es válida."

class ValidateEndDate:
    ERROR_MSG = "La fecha de finalización debe ser posterior a la fecha de inicio."

class ValidatePassword:
    ERROR_MSG = "La contraseña debe contener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial."
    PASSWORD_SPECIAL_CHAR = '@$!%*?&.'


