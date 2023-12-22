class UserStringLen:
    username = 20
    email = 50
    password = 128
    name = 50
    surname = 50
    
class CandidateStringLen:
    skills = 50

class CompanyStringLen:
    tin = 9
    company_name = 30

class LanguageStringLen:
    name = 30

class SectorStringLen:
    category = 30
    subcategory = 30

class ExperienceStringLen:
    company_name = 30
    position = 30
    position_description = 200

class EducationStringLen:
    qualification = 50

class EducationLevelStringLen:
    name = 30

class LanguageLevelStringLen:
    name = 30

class AddressStringLen:
    street = 50
    city = 50
    province = 50

class JobStringLen:
    title = 50
    description = 200
    skills = CandidateStringLen.skills