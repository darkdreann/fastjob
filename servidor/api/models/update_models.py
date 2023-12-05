from api.models.create_models import *

class UpdateAddress(CreateAddress):
    """Modelo para actualizar una direccion

        Atributos:
            postal_code: Codigo postal
            street: Calle de la direccion
            city: Ciudad de la direccion
            province: Provincia de la direccion"""


class UpdateUser(CreateUser):
    """Modelo para actualizar un usuario

        Atributos:
            username: nombre identificador del usuario
            email: Correo electronico
            name: Nombre del usuario
            surname: Apellido del usuario
            phone_numbers: Lista de numeros de telefono
            password: Contraseña del usuario
            address: Direccion del usuario"""


class UpdateCandidate(CreateCandidate):
    """Modelo para actualizar un candidato

        Atributos:
            username: nombre identificador del usuario
            email: Correo electronico
            name: Nombre del usuario
            surname: Apellido del usuario
            phone_numbers: Lista de numeros de telefono
            password: Contraseña del usuario
            address: Direccion del usuario
            skills: Lista de habilidades del candidato
            availability: Lista de disponibilidad de jornada laboral del candidato"""
    
class UpdateCompany(CreateCompany):
    """Modelo para actualizar una empresa

        Atributos:
            username: nombre identificador del usuario
            email: Correo electronico
            name: Nombre del usuario
            surname: Apellido del usuario
            phone_numbers: Lista de numeros de telefono
            password: Contraseña del usuario
            address: Direccion del usuario
            tin: Numero de identificacion de la empresa
            company_name: Nombre de la empresa"""

class UpdateLanguage(CreateLanguage):
    """Modelo para actualizar un idioma

        Atributos:
            name: Nombre del idioma"""
    

class UpdateSector(CreateSector):
    """Modelo para actualizar un sector

        Atributos:
            category: Categoria del sector
            subcategory: Subcategoria del sector"""
    
class UpdateExperience(CreateExperience):
    """Modelo para actualizar una experiencia

        Atributos:
            company_name: Nombre de la empresa
            position: Puesto de trabajo
            position_description: Descripcion del puesto de trabajo
            start_date: Fecha de inicio
            end_date: Fecha de finalizacion
            sector_id: Sector de la experiencia"""
    

class UpdateEducation(CreateEducation):
    """Modelo para actualizar una formacion

        Atributos:
            qualification: Titulo de la formacion
            level_id: Nivel de la formacion
            sector_id: Sector de la formacion si lo tiene"""
    

class UpdateLevel(CreateLevel):
    """Modelo para actualizar un nivel de formacion o idioma

        Atributos:
            name: Nombre del nivel de formacion o idioma
            value: Valor numerico del nivel de formacion o idioma"""
    
class UpdateJob(CreateJob):
    """Modelo para actualizar una oferta

        Atributos:
            title: Titulo del puesto de trabajo (ejemplo: Desarrollador web)
            description: Descripcion del puesto de trabajo
            skills: Lista de habilidades requeridas para el trabajo
            work_schedule: Disponibilidad de jornada laboral requerida
            required_experience_months: Experiencia requerida en meses
            active: Estado de la oferta de trabajo (abierta o cerrada))
            address: Direccion de la oferta
            required_education_level_id: Nivel de formacion requerido
            sector_id: Sector de la oferta
            company_id: Empresa que publica la oferta"""
    
