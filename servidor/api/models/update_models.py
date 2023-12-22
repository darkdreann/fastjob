from api.models.create_models import *

class UpdateAddress(CreateAddress):
    """
    Modelo para actualizar una dirección

    Atributos:
    - postal_code: Código postal
    - street: Calle de la dirección
    - city: Ciudad de la dirección
    - province: Provincia de la dirección
    """


class UpdateUser(CreateUser):
    """
    Modelo para actualizar un usuario

    Atributos:
    - username: Nombre identificador del usuario
    - email: Correo electrónico
    - name: Nombre del usuario
    - surname: Apellido del usuario
    - phone_numbers: Lista de números de teléfono
    - password: Contraseña del usuario
    - address: Dirección del usuario
    """


class UpdateCandidate(CreateCandidate):
    """
    Modelo para actualizar un candidato

    Atributos:
    - username: Nombre identificador del usuario
    - email: Correo electrónico
    - name: Nombre del usuario
    - surname: Apellido del usuario
    - phone_numbers: Lista de números de teléfono
    - password: Contraseña del usuario
    - address: Dirección del usuario
    - skills: Lista de habilidades del candidato
    - availability: Lista de disponibilidad de jornada laboral del candidato
    """
    
class UpdateCompany(CreateCompany):
    """
    Modelo para actualizar una empresa

    Atributos:
    - username: Nombre identificador del usuario
    - email: Correo electrónico
    - name: Nombre del usuario
    - surname: Apellido del usuario
    - phone_numbers: Lista de números de teléfono
    - password: Contraseña del usuario
    - address: Dirección del usuario
    - tin: Número de identificación de la empresa
    - company_name: Nombre de la empresa
    """

class UpdateLanguage(CreateLanguage):
    """
    Modelo para actualizar un idioma

    Atributos:
    - name: Nombre del idioma
    """
    

class UpdateSector(CreateSector):
    """
    Modelo para actualizar un sector

    Atributos:
    - category: Categoría del sector
    - subcategory: Subcategoría del sector
    """
    
class UpdateExperience(CreateExperience):
    """
    Modelo para actualizar una experiencia

    Atributos:
    - company_name: Nombre de la empresa
    - position: Puesto de trabajo
    - position_description: Descripción del puesto de trabajo
    - start_date: Fecha de inicio
    - end_date: Fecha de finalización
    - sector_id: Sector de la experiencia
    """
    

class UpdateEducation(CreateEducation):
    """
    Modelo para actualizar una formación

    Atributos:
    - qualification: Título de la formación
    - level_id: Nivel de la formación
    - sector_id: Sector de la formación si lo tiene
    """
    

class UpdateLevel(CreateLevel):
    """
    Modelo para actualizar un nivel de formación o idioma

    Atributos:
    - name: Nombre del nivel de formación o idioma
    - value: Valor numérico del nivel de formación o idioma
    """
    
class UpdateJob(CreateJob):
    """
    Modelo para actualizar una oferta

    Atributos:
    - title: Título del puesto de trabajo
    - description: Descripción del puesto de trabajo
    - skills: Lista de habilidades requeridas para el trabajo
    - work_schedule: Disponibilidad de jornada laboral requerida
    - required_experience_months: Experiencia requerida en meses
    - active: Estado de la oferta de trabajo (abierta o cerrada))
    - address: Dirección de la oferta
    - required_education: Formación requerida
    - sector_id: Sector de la oferta
    - company_id: Empresa que publica la oferta
    """
