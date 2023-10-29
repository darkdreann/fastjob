from typing import Optional, Self
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID
from datetime import date
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, Enum, String, Integer, ARRAY, CheckConstraint, UniqueConstraint, text, select
from sqlalchemy.orm import Mapped, DeclarativeBase, relationship, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.database_models.metadata.table_name import *
from api.database.database_models.metadata.constraint_name import *
from api.database.database_models.metadata.string_length import *
from api.models.enums import UserType, WorkSchedule
from api.models.create_models import CreateAdress
from api.security.hash_crypt import encrypt_string

class Base(DeclarativeBase):
    pass

class JobCandidate(Base):
    """Modelo de la tabla jobcandidate.
    
    Esta tabla representa la relación entre las tablas job y candidate.
    
    Campos:
        candidate_id: Campo que representa la clave foránea de la tabla candidate.
        job_id: Campo que representa la clave foránea de la tabla job."""

    __tablename__ = JOB_CANDIDATE

    candidate_id: Mapped[UUID] = mapped_column(ForeignKey(f"{CANDIDATE}.user_id", name=JobCandidateConstraint.CANDIDATE_FK, ondelete="CASCADE"))
    job_id: Mapped[UUID] = mapped_column(ForeignKey(f"{JOB}.id", name=JobCandidateConstraint.JOB_FK))
    compatibility: Mapped[float]

    candidate: Mapped["Candidate"] = relationship(back_populates="applied_jobs_list")
    job: Mapped["Job"] = relationship(back_populates="candidates_list")

    __table_args__ = (
        PrimaryKeyConstraint(candidate_id, job_id, name=JobCandidateConstraint.JOB_CANDIDATE_PK),
    )


class SectorEducation(Base):
    """Modelo de la tabla sector_education.

    Esta tabla representa la relación entre las tablas sector y education.

    Campos:
        education_id: Campo que representa la clave foránea de la tabla education.
        sector_id: Campo que representa la clave foránea de la tabla sector."""

    __tablename__ = SECTOR_EDUCATION

    education_id: Mapped[UUID] = mapped_column(ForeignKey(f"{EDUCATION}.id", name=SectorEducationConstraint.EDUCATION_FK))
    sector_id: Mapped[UUID] = mapped_column(ForeignKey(f"{SECTOR}.id", name=SectorEducationConstraint.SECTOR_FK))

    sector: Mapped["Sector"] = relationship(back_populates="education_list")
    education: Mapped["Education"] = relationship(back_populates="sector")

    __table_args__ = (
        PrimaryKeyConstraint(education_id, sector_id, name=SectorEducationConstraint.SECTOR_EDUCATION_PK),
    )


class CandidateEducation(Base):
    """Modelo de la tabla candidate_education.

    Esta tabla representa la relación entre las tablas candidate y education.

    Campos:
        candidate_id: Campo que representa la clave foránea de la tabla candidate.
        education_id: Campo que representa la clave foránea de la tabla education.
        completion_date: Campo que representa la fecha de finalización de los estudios.
        
    Relaciones:
        candidate: Relación con la tabla candidate.
        education: Relación con la tabla education."""

    __tablename__ = CANDIDATE_EDUCATION

    candidate_id: Mapped[UUID] = mapped_column(ForeignKey(f"{CANDIDATE}.user_id", name=CandidateEducationConstraint.CANDIDATE_FK, ondelete="CASCADE"))
    education_id: Mapped[UUID] = mapped_column(ForeignKey(f"{EDUCATION}.id", name=CandidateEducationConstraint.EDUCATION_FK))
    completion_date: Mapped[date]

    candidate: Mapped["Candidate"] = relationship(back_populates="education_list")
    education: Mapped["Education"] = relationship(back_populates="candidates_list")

    __table_args__ = (
        PrimaryKeyConstraint(candidate_id, education_id, name=CandidateEducationConstraint.CANDIDATE_EDUCATION_PK),
    )


class CandidateLanguage(Base):
    """Modelo de la tabla candidate_language.

    Esta tabla representa la relación entre las tablas candidate y language, Además, contiene la relación con la tabla language_level que representa el nivel de idioma del candidato.

    Campos:
        candidate_id: Campo que representa la clave foránea de la tabla candidate.
        language_id: Campo que representa la clave foránea de la tabla language.
        language_level_id: Campo que representa la clave foránea de la tabla language_level.

    Relaciones:
        candidate: Relación con la tabla candidate.
        language: Relación con la tabla language.
        language_level: Relación con la tabla language_level."""

    __tablename__ = CANDIDATE_LANGUAGE

    candidate_id: Mapped[UUID] = mapped_column(ForeignKey(f"{CANDIDATE}.user_id", name=CandidateLanguageConstraint.CANDIDATE_FK, ondelete="CASCADE"))
    language_id: Mapped[UUID] = mapped_column(ForeignKey(f"{LANGUAGE}.id", name=CandidateLanguageConstraint.LANGUAGE_FK))
    language_level_id: Mapped[UUID] = mapped_column(ForeignKey(f"{LANGUAGE_LEVEL}.id", name=CandidateLanguageConstraint.LANGUAGE_LEVEL_FK))

    candidate: Mapped["Candidate"] = relationship(back_populates="language_list")
    language: Mapped["Language"] = relationship(back_populates="candidates_list")
    language_level: Mapped["LanguageLevel"] = relationship(back_populates="candidates_language_list")

    __table_args__ = (
        PrimaryKeyConstraint(candidate_id, language_id, name=CandidateLanguageConstraint.CANDIDATE_LANGUAGE_PK),
    )

class JobLanguage(Base):
    """Modelo de la tabla job_language.

    Esta tabla representa la relación entre las tablas job y language, Además, contiene la relación con la tabla language_level que representa el nivel de idioma requerido por la oferta de trabajo.

    Campos:
        job_id: Campo que representa la clave foránea de la tabla job.
        language_id: Campo que representa la clave foránea de la tabla language.
        language_level_id: Campo que representa la clave foránea de la tabla language_level.
    
    Relaciones:
        job: Relación con la tabla job.
        language: Relación con la tabla language.
        language_level: Relación con la tabla language_level."""

    __tablename__ = JOB_LANGUAGE

    job_id: Mapped[UUID] = mapped_column(ForeignKey(f"{JOB}.id", name=JobLanguageConstraint.JOB_FK, ondelete="CASCADE"))
    language_id: Mapped[UUID] = mapped_column(ForeignKey(f"{LANGUAGE}.id", name=JobLanguageConstraint.LANGUAGE_FK))
    language_level_id: Mapped[UUID] = mapped_column(ForeignKey(f"{LANGUAGE_LEVEL}.id", name=JobLanguageConstraint.LANGUAGE_LEVEL_FK))

    job: Mapped["Job"] = relationship(back_populates="language_list")
    language: Mapped["Language"] = relationship(back_populates="jobs_list")
    language_level: Mapped["LanguageLevel"] = relationship(back_populates="jobs_language_list")

    __table_args__ = (
        PrimaryKeyConstraint(job_id, language_id, name=JobLanguageConstraint.JOB_LANGUAGE_PK),
    )

#################################################################################################################################

class User(Base):
    """Modelo de la tabla user.

    Esta tabla representa a los usuarios de la aplicación.

    Campos:
        id: Campo que representa la clave primaria de la tabla.
        user_type: Campo que representa el tipo de usuario.
        username: Campo que representa el nombre de usuario.
        email: Campo que representa el correo electrónico.
        password: Campo que representa la contraseña.
        name: Campo que representa el nombre del usuario.
        surname: Campo que representa el apellido del usuario.
        phone_numbers: Campo que representa los números de teléfono del usuario.
        adress_postal_code: Campo que representa el código postal de la dirección del usuario.
    
    Relaciones:
        adress: Relación con la tabla adress.
        candidate: Relación con la tabla candidate.
        company: Relación con la tabla company."""

    __tablename__ = USER

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType))
    username: Mapped[str] = mapped_column(String(UserStringLen.username), index=True)
    email: Mapped[str] = mapped_column(String(UserStringLen.email), index=True)
    _password: Mapped[str] = mapped_column(String(UserStringLen.password), name="password")
    name: Mapped[str] = mapped_column(String(UserStringLen.name))
    surname: Mapped[str] = mapped_column(String(UserStringLen.surname))
    phone_numbers: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    adress_id: Mapped[UUID] = mapped_column(ForeignKey(f"{ADRESS}.id", name=UserConstraint.ADRESS_FK))
    
    adress: Mapped["Adress"] = relationship(back_populates="users_list")
    candidate: Mapped["Candidate"] = relationship(back_populates="user", uselist=False)
    company: Mapped["Company"] = relationship(back_populates="user", uselist=False)

    __table_args__ = (
        PrimaryKeyConstraint("id", name=UserConstraint.USER_PK),
        UniqueConstraint("email", name=UserConstraint.DUPLICATE_EMAIL),
        UniqueConstraint("username", name=UserConstraint.DUPLICATE_USERNAME),
        CheckConstraint(
            text(f"NOT (user_type = '{UserType.ADMIN.value}' AND (check_has_table_candidate(id) OR check_has_table_company(id)))"),
            name=UserConstraint.ADMIN_HAS_TABLE
        ),
        CheckConstraint(
            text(f"NOT (user_type = '{UserType.COMPANY.value}' AND check_has_table_candidate(id))"),
            name=UserConstraint.COMPANY_HAS_CANDIDATE_TABLE
        ),
        CheckConstraint(
            text(f"NOT (user_type = '{UserType.CANDIDATE.value}' AND check_has_table_company(id))"),
            name=UserConstraint.CANDIDATE_HAS_COMPANY_TABLE
        ),
    )

    @property
    def password(self):
        """Devuelve la contraseña encriptada."""	

        return self._password

    @password.setter
    def password(self, password):
        """Encripta la contraseña y la guarda."""

        self._password = encrypt_string(password)


class Candidate(Base):
    """Modelo de la tabla candidate.

    Esta tabla representa a los candidatos de la aplicación.

    Campos:
        user_id: Campo que representa la clave foránea de la tabla user.
        skills: Campo que representa las habilidades del candidato.
        availability: Campo que representa la disponibilidad del candidato.
    
    Relaciones:
        user: Relación con la tabla user.
        education_list: Relación con la tabla candidate_education.
        language_list: Relación con la tabla candidate_language.
        experience_list: Relación con la tabla experience.
        applied_jobs_list: Relación con la tabla job."""

    __tablename__ = CANDIDATE

    user_id: Mapped[UUID] = mapped_column(ForeignKey(f"{USER}.id", name=CandidateConstraint.USER_FK, ondelete="CASCADE"))
    skills: Mapped[list[str]] = mapped_column(ARRAY(String(CandidateStringLen.skills)))
    availability: Mapped[list[WorkSchedule]] = mapped_column(ARRAY(Enum(WorkSchedule)))
    curriculum: Mapped[Optional[bytes]]

    user: Mapped["User"] = relationship(back_populates="candidate", uselist=False)
    education_list: Mapped[list["CandidateEducation"]] = relationship(back_populates="candidate")
    language_list: Mapped[list["CandidateLanguage"]] = relationship(back_populates="candidate")
    experience_list: Mapped[list["Experience"]] = relationship(back_populates="candidate")
    applied_jobs_list: Mapped[list["JobCandidate"]] = relationship(back_populates="candidate")

    __table_args__ = (
        PrimaryKeyConstraint(user_id, name=CandidateConstraint.CANDIDATE_PK),
        CheckConstraint(
            text(f"check_user_type(user_id, '{UserType.CANDIDATE.value}')"),
            name=CandidateConstraint.USER_NOT_CANDIDATE
        ),
    )


class Company(Base):
    """Modelo de la tabla company.

    Esta tabla representa a las empresas de la aplicación.

    Campos:
        user_id: Campo que representa la clave foránea de la tabla user.
        tin: Campo que representa el CIF de la empresa.
        company_name: Campo que representa el nombre de la empresa.

    Relaciones:
        user: Relación con la tabla user.
        job_list: Relación con la tabla job."""

    __tablename__ = COMPANY

    user_id: Mapped[UUID] = mapped_column(ForeignKey(f"{USER}.id", name=CompanyConstraint.USER_FK, ondelete="CASCADE"))
    tin: Mapped[str] = mapped_column(String(CompanyStringLen.tin))
    company_name: Mapped[str] = mapped_column(String(CompanyStringLen.company_name))

    user: Mapped["User"] = relationship(back_populates="company", uselist=False)
    job_list: Mapped[list["Job"]] = relationship(back_populates="company")

    __table_args__ = (
        PrimaryKeyConstraint(user_id, name=CompanyConstraint.COMPANY_PK),
        UniqueConstraint("tin", name=CompanyConstraint.DUPLICATE_TIN),
        UniqueConstraint("company_name", name=CompanyConstraint.DUPLICATE_COMPANY_NAME),
        CheckConstraint(
            text(f"check_user_type(user_id, '{UserType.COMPANY.value}')"),
            name=CompanyConstraint.USER_NOT_COMPANY
        ),
    )

class Language(Base):
    """Modelo de la tabla language.

    Esta tabla representa los idiomas de la aplicación.

    Campos:
        id: Campo que representa la clave primaria de la tabla.
        name: Campo que representa el nombre del idioma.
    
    Relaciones:
        candidates_list: Relación con la tabla candidate_language.
        jobs_list: Relación con la tabla job_language."""

    __tablename__ = LANGUAGE

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    name: Mapped[str] = mapped_column(String(LanguageStringLen.name))
    
    candidates_list: Mapped[list["CandidateLanguage"]] = relationship(back_populates="language")
    jobs_list: Mapped[list["JobLanguage"]] = relationship(back_populates="language")

    __table_args__ = (
        PrimaryKeyConstraint("id", name=LanguageConstraint.LANGUAGE_PK),
        UniqueConstraint(name, name=LanguageConstraint.DUPLICATE_LANGUAGE_NAME),
    )

class Sector(Base):
    """Modelo de la tabla sector.

    Esta tabla representa los sectores de la aplicación.

    Campos:
        id: Campo que representa la clave primaria de la tabla.
        category: Campo que representa la categoría del sector.
        subcategory: Campo que representa la subcategoría del sector.
    
    Relaciones:
        education_list: Relación con la tabla sector_education.
        experience_list: Relación con la tabla experience."""

    __tablename__ = SECTOR

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    category: Mapped[str] = mapped_column(String(SectorStringLen.category), index=True)
    subcategory: Mapped[str] = mapped_column(String(SectorStringLen.subcategory))

    education_list: Mapped[list["SectorEducation"]] = relationship(back_populates="sector")
    experience_list: Mapped[list["Experience"]] = relationship(back_populates="sector")
    job_list: Mapped[list["Job"]] = relationship(back_populates="sector")
    

    __table_args__ = (
        PrimaryKeyConstraint("id", name=SectorConstraint.SECTOR_PK),
        UniqueConstraint(category, subcategory, name=SectorConstraint.DUPLICATE_CATEGORY_SUBCATEGORY),
    )

class Experience(Base):
    """Modelo de la tabla experience.

    Esta tabla representa la experiencia de los candidatos.

    Campos:
        id: Campo que representa la clave primaria de la tabla.
        company_name: Campo que representa el nombre de la empresa.
        start_date: Campo que representa la fecha de inicio.
        end_date: Campo que representa la fecha de finalización.
        job_position: Campo que representa el puesto de trabajo.
        job_position_description: Campo que representa la descripción del puesto de trabajo.
        candidate_id: Campo que representa la clave foránea de la tabla candidate.
        sector_id: Campo que representa la clave foránea de la tabla sector.

    Relaciones:
        candidate: Relación con la tabla candidate.
        sector: Relación con la tabla sector."""

    __tablename__ = EXPERIENCE

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    company_name: Mapped[str] = mapped_column(String(ExperienceStringLen.company_name))
    start_date: Mapped[date]
    end_date: Mapped[date]
    job_position: Mapped[str] = mapped_column(String(ExperienceStringLen.position))
    job_position_description: Mapped[str] = mapped_column(String(ExperienceStringLen.position_description))
    candidate_id: Mapped[UUID] = mapped_column(ForeignKey(f"{CANDIDATE}.user_id", name=ExperienceConstraint.CANDIDATE_FK, ondelete="CASCADE"))
    sector_id: Mapped[UUID] = mapped_column(ForeignKey(f"{SECTOR}.id", name=ExperienceConstraint.SECTOR_FK))

    candidate: Mapped["Candidate"] = relationship(back_populates="experience_list")
    sector: Mapped["Sector"] = relationship(back_populates="experience_list")

    __table_args__ = (
        PrimaryKeyConstraint("id", name=ExperienceConstraint.EXPERIENCE_PK),
    )

class Education(Base):
    """Modelo de la tabla education.

    Esta tabla representa la educación de los candidatos.

    Campos:
        id: Campo que representa la clave primaria de la tabla.
        qualification: Campo que representa la cualificación.
        level_id: Campo que representa la clave foránea de la tabla education_level.
        sector_id: Campo que representa la clave foránea de la tabla sector.
    
    Relaciones:
        sector: Relación con la tabla sector.
        level: Relación con la tabla education_level.
        candidates_list: Relación con la tabla candidate_education."""
    
    __tablename__ = EDUCATION

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    qualification: Mapped[str] = mapped_column(String(EducationStringLen.qualification))
    level_id: Mapped[UUID] = mapped_column(ForeignKey(f"{EDUCATION_LEVEL}.id", name=EducationConstraint.LEVEL_FK))

    sector: Mapped[Optional["SectorEducation"]] = relationship(back_populates="education")
    level: Mapped["EducationLevel"] = relationship(back_populates="education_list")
    candidates_list: Mapped[list["CandidateEducation"]] = relationship(back_populates="education")

    __table_args__ = (
        PrimaryKeyConstraint("id", name=EducationConstraint.EDUCATION_PK),
        UniqueConstraint(qualification, name=EducationConstraint.DUPLICATE_QUALIFICATION),
    )

class EducationLevel(Base):
    """Modelo de la tabla education_level.

    Esta tabla representa los niveles de educación de los candidatos.

    Campos:
        id: Campo que representa la clave primaria de la tabla.
        value: Campo que representa el valor del nivel de educación.
        name: Campo que representa el nombre del nivel de educación.

    Relaciones:
        education_list: Relación con la tabla education
        jobs_list: Relación con la tabla job."""

    __tablename__ = EDUCATION_LEVEL

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    value: Mapped[int]
    name: Mapped[str] = mapped_column(String(EducationLevelStringLen.name))

    education_list: Mapped[list["Education"]] = relationship(back_populates="level")
    jobs_list: Mapped[list["Job"]] = relationship(back_populates="education_level")

    __table_args__ = (
        PrimaryKeyConstraint("id", name=EducationLevelConstraint.EDUCATION_LEVEL_PK),
        UniqueConstraint("value", name=EducationLevelConstraint.DUPLICATE_VALUE),
        UniqueConstraint(name, name=EducationLevelConstraint.DUPLICATE_NAME)
    )


class LanguageLevel(Base):
    """Modelo de la tabla language_level.

    Esta tabla representa los niveles de idioma de los candidatos.

    Campos:
        id: Campo que representa la clave primaria de la tabla.
        value: Campo que representa el valor del nivel de idioma.
        name: Campo que representa el nombre del nivel de idioma.

    Relaciones:
        candidates_language_list: Relación con la tabla candidate_language
        jobs_language_list: Relación con la tabla job_language."""

    __tablename__ = LANGUAGE_LEVEL

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    value: Mapped[int]
    name: Mapped[str] = mapped_column(String(LanguageLevelStringLen.name))

    candidates_language_list: Mapped[list["CandidateLanguage"]] = relationship(back_populates="language_level")
    jobs_language_list: Mapped[list["JobLanguage"]] = relationship(back_populates="language_level")

    __table_args__ = (
        PrimaryKeyConstraint("id", name=LanguageLevelConstraint.LANGUAGE_LEVEL_PK),
        UniqueConstraint("value", name=LanguageLevelConstraint.DUPLICATE_VALUE),
        UniqueConstraint(name, name=LanguageLevelConstraint.DUPLICATE_NAME)
    )

class Adress(Base):
    """Modelo de la tabla adress.

    Esta tabla representa las direcciones de los usuarios.

    Campos:
        id: Campo que representa la clave primaria de la tabla.
        postal_code: Campo que representa el código postal.
        street: Campo que representa la calle.
        city: Campo que representa la ciudad.
        province: Campo que representa la provincia.
    
    Relaciones:
        users_list: Relación con la tabla user.
        jobs_list: Relación con la tabla job."""

    __tablename__ = ADRESS

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    postal_code: Mapped[int] = mapped_column(Integer, index=True)
    street: Mapped[str] = mapped_column(String(AdressStringLen.street))
    city: Mapped[str] = mapped_column(String(AdressStringLen.city))
    province: Mapped[str] = mapped_column(String(AdressStringLen.province))

    users_list: Mapped[list["User"]] = relationship(back_populates="adress")
    jobs_list: Mapped[list["Job"]] = relationship(back_populates="adress")

    __table_args__ = (
        PrimaryKeyConstraint("id", name=AdressConstraint.ADRESS_PK),
        UniqueConstraint(postal_code, name=AdressConstraint.DUPLICATE_POSTAL_CODE),
        UniqueConstraint(postal_code, city, province, name=AdressConstraint.DUPLICATE_ADRESS)
    )

    @classmethod
    async def get_adress(cls, session: AsyncSession, adress: CreateAdress) -> Self:
        """Obtiene una direccion de la base de datos a partir de una dirección. Si no existe devuelve la dirección pasada por parametro.
        
            Args:
                session (AsyncSession): Sesión abierta con la base de datos.
                adress (CreateAdress): Dirección a buscar en la base de datos.
                
            Returns:
                Adress: Dirección encontrada en la base de datos o la dirección pasada por parametro."""

        statement = select(cls).where(cls.postal_code == adress.postal_code)
        result = await session.execute(statement)
        adress_from_db = result.scalars().first()
        
        if adress_from_db is None:
            adress_from_db = Adress(**adress.model_dump())

        return adress_from_db

class Job(Base):
    """Modelo de la tabla job.

    Esta tabla representa las ofertas de trabajo.

    Campos:
        id: Campo que representa la clave primaria de la tabla.
        title: Campo que representa el título de la oferta.
        description: Campo que representa la descripción de la oferta.
        required_months_of_experience: Campo que representa los meses de experiencia requeridos.
        work_schedule: Campo que representa el horario de trabajo.
        skills: Campo que representa las habilidades requeridas.
        active: Campo que representa si la oferta está activa.
        publication_date: Campo que representa la fecha de publicación.
        adress_postal_code: Campo que representa el código postal de la dirección de la oferta.
        company_id: Campo que representa la clave foránea de la tabla company.
        education_level_id: Campo que representa la clave foránea de la tabla education_level.
        sector_id: Campo que representa la clave foránea de la tabla sector.

    Relaciones:
        company: Relación con la tabla company.
        education_level: Relación con la tabla education_level.
        adress: Relación con la tabla adress.
        language_list: Relación con la tabla job_language.
        candidate: Relación con la tabla candidate."""

    __tablename__ = JOB

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    title: Mapped[str] = mapped_column(String(JobStringLen.title))
    description: Mapped[str] = mapped_column(String(JobStringLen.description))
    required_months_of_experience: Mapped[int]
    work_schedule: Mapped[WorkSchedule] = mapped_column(Enum(WorkSchedule))
    skills: Mapped[list[str]] = mapped_column(ARRAY(String(JobStringLen.skills)))
    active: Mapped[bool]
    publication_date: Mapped[date]
    adress_id: Mapped[UUID] = mapped_column(ForeignKey(f"{ADRESS}.id", name=JobConstraint.ADRESS_FK))
    company_id: Mapped[UUID] = mapped_column(ForeignKey(f"{COMPANY}.user_id", name=JobConstraint.COMPANY_FK, ondelete="CASCADE"))
    education_level_id: Mapped[UUID] = mapped_column(ForeignKey(f"{EDUCATION_LEVEL}.id", name=JobConstraint.LEVEL_EDUCATION_FK))
    sector_id: Mapped[UUID] = mapped_column(ForeignKey(f"{SECTOR}.id", name=JobConstraint.SECTOR_FK))
    
    company: Mapped["Company"] = relationship(back_populates="job_list")
    education_level: Mapped["EducationLevel"] = relationship(back_populates="jobs_list")
    adress: Mapped["Adress"] = relationship(back_populates="jobs_list")
    language_list: Mapped[list["JobLanguage"]] = relationship(back_populates="job")
    candidates_list: Mapped[list["JobCandidate"]] = relationship(back_populates="job")
    sector: Mapped["Sector"] = relationship(back_populates="job_list")

    __table_args__ = (
        PrimaryKeyConstraint("id", name=JobConstraint.JOB_PK),
    )
