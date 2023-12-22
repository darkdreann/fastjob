from typing import Optional
from uuid import uuid4, UUID
from datetime import date, timedelta
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID, ARRAY, INTERVAL
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, Enum, String, Integer, CheckConstraint, UniqueConstraint, text, Date, LargeBinary
from sqlalchemy.orm import Mapped, DeclarativeBase, relationship, mapped_column, deferred
from sqlalchemy.ext.hybrid import hybrid_property
from api.database.database_models.metadata.table_name import *
from api.database.database_models.metadata.constraint_name import *
from api.database.database_models.metadata.string_length import *
from api.models.metadata.constants import MONTHS_TO_DAYS_MULTIPLIER
from api.models.enums.models import UserType, WorkSchedule
from api.security.hash_crypt import encrypt_string

class Base(DeclarativeBase):
    pass

class SectorEducation(Base):
    """
    Modelo de la tabla sector_education.

    Esta tabla representa la relación entre las tablas sector y education.

    Campos:
    - education_id: Campo que representa la clave foránea de la tabla education.
    - sector_id: Campo que representa la clave foránea de la tabla sector.
    
    Relaciones:
    - sector: Relación con la tabla sector.
    - education: Relación con la tabla education.
    """

    __tablename__ = SECTOR_EDUCATION

    education_id: Mapped[UUID] = mapped_column(ForeignKey(f"{EDUCATION}.id", name=SectorEducationConstraint.EDUCATION_FK, ondelete="CASCADE"))
    sector_id: Mapped[UUID] = mapped_column(ForeignKey(f"{SECTOR}.id", name=SectorEducationConstraint.SECTOR_FK))

    sector: Mapped["Sector"] = relationship(back_populates="education_list", lazy="joined")
    education: Mapped["Education"] = relationship(back_populates="sector", lazy="joined")

    __table_args__ = (
        PrimaryKeyConstraint(education_id, sector_id, name=SectorEducationConstraint.SECTOR_EDUCATION_PK),
        UniqueConstraint(education_id, name=SectorEducationConstraint.DUPLICATE_EDUCATION_ID),
    )


class CandidateEducation(Base):
    """
    Modelo de la tabla candidate_education.

    Esta tabla representa la relación entre las tablas candidate y education.

    Campos:
    - candidate_id: Campo que representa la clave foránea de la tabla candidate.
    - education_id: Campo que representa la clave foránea de la tabla education.
    - completion_date: Campo que representa la fecha de finalización de los estudios.
        
    Relaciones:
    - candidate: Relación con la tabla candidate.
    - education: Relación con la tabla education.
    """

    __tablename__ = CANDIDATE_EDUCATION

    candidate_id: Mapped[UUID] = mapped_column(ForeignKey(f"{CANDIDATE}.user_id", name=CandidateEducationConstraint.CANDIDATE_FK, ondelete="CASCADE"))
    education_id: Mapped[UUID] = mapped_column(ForeignKey(f"{EDUCATION}.id", name=CandidateEducationConstraint.EDUCATION_FK))
    completion_date: Mapped[date]

    candidate: Mapped["Candidate"] = relationship(back_populates="education_list", lazy="joined")
    education: Mapped["Education"] = relationship(back_populates="candidates_list", lazy="joined")

    __table_args__ = (
        PrimaryKeyConstraint(candidate_id, education_id, name=CandidateEducationConstraint.CANDIDATE_EDUCATION_PK),
    )


class CandidateLanguage(Base):
    """
    Modelo de la tabla candidate_language.

    Esta tabla representa la relación entre las tablas candidate y language, Además, contiene la relación con la tabla language_level que representa el nivel de idioma del candidato.

    Campos:
    - candidate_id: Campo que representa la clave foránea de la tabla candidate.
    - language_id: Campo que representa la clave foránea de la tabla language.
    - language_level_id: Campo que representa la clave foránea de la tabla language_level.

    Relaciones:
    - candidate: Relación con la tabla candidate.
    - language: Relación con la tabla language.
    - language_level: Relación con la tabla language_level.
    """

    __tablename__ = CANDIDATE_LANGUAGE

    candidate_id: Mapped[UUID] = mapped_column(ForeignKey(f"{CANDIDATE}.user_id", name=CandidateLanguageConstraint.CANDIDATE_FK, ondelete="CASCADE"))
    language_id: Mapped[UUID] = mapped_column(ForeignKey(f"{LANGUAGE}.id", name=CandidateLanguageConstraint.LANGUAGE_FK))
    language_level_id: Mapped[UUID] = mapped_column(ForeignKey(f"{LANGUAGE_LEVEL}.id", name=CandidateLanguageConstraint.LANGUAGE_LEVEL_FK))

    candidate: Mapped["Candidate"] = relationship(back_populates="language_list", lazy="joined")
    language: Mapped["Language"] = relationship(back_populates="candidates_list", lazy="joined")
    language_level: Mapped["LanguageLevel"] = relationship(back_populates="candidates_language_list", lazy="joined", order_by="LanguageLevel.value.desc()")

    __table_args__ = (
        PrimaryKeyConstraint(candidate_id, language_id, name=CandidateLanguageConstraint.CANDIDATE_LANGUAGE_PK),
    )
class JobCandidate(Base):
    """
    Modelo de la tabla jobcandidate.
    
    Esta tabla representa la relación entre las tablas job y candidate.
    
    Campos:
    - candidate_id: Campo que representa la clave foránea de la tabla candidate.
    - job_id: Campo que representa la clave foránea de la tabla job.
    - inscription_date: Campo que representa la fecha de inscripción a la oferta.
    
    Relaciones:
    - candidate: Relación con la tabla candidate.
    - job: Relación con la tabla job.
    """

    __tablename__ = JOB_CANDIDATE

    candidate_id: Mapped[UUID] = mapped_column(ForeignKey(f"{CANDIDATE}.user_id", name=JobCandidateConstraint.CANDIDATE_FK, ondelete="CASCADE"))
    job_id: Mapped[UUID] = mapped_column(ForeignKey(f"{JOB}.id", name=JobCandidateConstraint.JOB_FK, ondelete="CASCADE"))
    inscription_date: Mapped[Optional[date]] = mapped_column(Date, server_default=text("CURRENT_DATE"))

    candidate: Mapped["Candidate"] = relationship(back_populates="applied_jobs_list", lazy="joined")
    job: Mapped["Job"] = relationship(back_populates="candidates_list", lazy="joined")

    __table_args__ = (
        PrimaryKeyConstraint(candidate_id, job_id, name=JobCandidateConstraint.JOB_CANDIDATE_PK),
    )

class JobEducation(Base):
    """
    Modelo de la tabla job_education.

    Esta tabla representa la relación entre las tablas job y education.

    Campos:
    - job_id: Campo que representa la clave foránea de la tabla job.
    - education_id: Campo que representa la clave foránea de la tabla education.

    Relaciones:
    - job: Relación con la tabla job.
    - education: Relación con la tabla education.
    """

    __tablename__ = JOB_EDUCATION

    job_id: Mapped[UUID] = mapped_column(ForeignKey(f"{JOB}.id", name=JobEducationConstraint.JOB_FK, ondelete="CASCADE"))
    education_id: Mapped[UUID] = mapped_column(ForeignKey(f"{EDUCATION}.id", name=JobEducationConstraint.EDUCATION_FK))

    job: Mapped["Job"] = relationship(back_populates="required_education", lazy="joined")
    education: Mapped["Education"] = relationship(back_populates="jobs_list", lazy="joined")

    __table_args__ = (
        PrimaryKeyConstraint(education_id, job_id, name=JobEducationConstraint.JOB_EDUCATION_PK),
        UniqueConstraint(job_id, name=JobEducationConstraint.DUPLICATE_JOB_ID),
    )

class JobLanguage(Base):
    """
    Modelo de la tabla job_language.

    Esta tabla representa la relación entre las tablas job y language, Además, contiene la relación con la tabla language_level que representa el nivel de idioma requerido por la oferta de trabajo.

    Campos:
    - job_id: Campo que representa la clave foránea de la tabla job.
    - language_id: Campo que representa la clave foránea de la tabla language.
    - language_level_id: Campo que representa la clave foránea de la tabla language_level.
    
    Relaciones:
    - job: Relación con la tabla job.
    - language: Relación con la tabla language.
    - language_level: Relación con la tabla language_level.
    """

    __tablename__ = JOB_LANGUAGE

    job_id: Mapped[UUID] = mapped_column(ForeignKey(f"{JOB}.id", name=JobLanguageConstraint.JOB_FK, ondelete="CASCADE"))
    language_id: Mapped[UUID] = mapped_column(ForeignKey(f"{LANGUAGE}.id", name=JobLanguageConstraint.LANGUAGE_FK))
    language_level_id: Mapped[UUID] = mapped_column(ForeignKey(f"{LANGUAGE_LEVEL}.id", name=JobLanguageConstraint.LANGUAGE_LEVEL_FK))

    job: Mapped["Job"] = relationship(back_populates="language_list", lazy="joined")
    language: Mapped["Language"] = relationship(back_populates="jobs_list", lazy="joined")
    language_level: Mapped["LanguageLevel"] = relationship(back_populates="jobs_language_list", lazy="joined")

    __table_args__ = (
        PrimaryKeyConstraint(job_id, language_id, name=JobLanguageConstraint.JOB_LANGUAGE_PK),
    )

#################################################################################################################################

class User(Base):
    """
    Modelo de la tabla user.

    Esta tabla representa a los usuarios de la aplicación.

    Campos:
    - id: Campo que representa la clave primaria de la tabla.
    - user_type: Campo que representa el tipo de usuario.
    - username: Campo que representa el nombre de usuario.
    - email: Campo que representa el correo electrónico.
    - password: Campo que representa la contraseña.
    - name: Campo que representa el nombre del usuario.
    - surname: Campo que representa el apellido del usuario.
    - phone_numbers: Campo que representa los números de teléfono del usuario.
    - address_id: Campo que representa la clave foránea de la tabla address.
    
    Relaciones:
    - address: Relación con la tabla address.
    - candidate: Relación con la tabla candidate.
    - company: Relación con la tabla company.
    """

    __tablename__ = USER

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType))
    _username: Mapped[str] = mapped_column(String(UserStringLen.username), index=True, name="username")
    _email: Mapped[str] = mapped_column(String(UserStringLen.email), index=True, name="email")
    _password: Mapped[str] = mapped_column(String(UserStringLen.password), name="password")
    _name: Mapped[str] = mapped_column(String(UserStringLen.name), name="name")
    _surname: Mapped[str] = mapped_column(String(UserStringLen.surname), name="surname")
    phone_numbers: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    address_id: Mapped[UUID] = mapped_column(ForeignKey(f"{ADDRESS}.id", name=UserConstraint.ADDRESS_FK))
    
    address: Mapped["Address"] = relationship(back_populates="users_list")
    candidate: Mapped[Optional["Candidate"]] = relationship(back_populates="user", uselist=False, lazy="noload")
    company: Mapped[Optional["Company"]] = relationship(back_populates="user", uselist=False, lazy="noload")

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

    @hybrid_property
    def username(self):
        """Devuelve el nombre de usuario."""

        return self._username
    
    @username.setter
    def username(self, username: str):
        """Guarda el nombre de usuario."""

        self._username = username.lower()

    @hybrid_property
    def password(self):
        """Devuelve la contrasena encriptada."""	

        return self._password

    @password.setter
    def password(self, password):
        """Encripta la contrasena y la guarda."""

        self._password = encrypt_string(password)

    @hybrid_property
    def email(self):
        """Devuelve el correo electronico."""

        return self._email
    
    @email.setter
    def email(self, email: str):
        """Guarda el correo electronico."""

        self._email = email.lower()

    @hybrid_property
    def name(self):
        """Devuelve el nombre."""

        return self._name
    
    @name.setter
    def name(self, name: str):
        """Guarda el nombre."""

        self._name = name.lower()

    @hybrid_property
    def surname(self):
        """Devuelve el apellido."""

        return self._surname

    @surname.setter
    def surname(self, surname: str):
        """Guarda el apellido."""

        self._surname = surname.lower()



class Candidate(Base):
    """
    Modelo de la tabla candidate.

    Esta tabla representa a los candidatos de la aplicación.

    Campos:
    - user_id: Campo que representa la clave foránea de la tabla user.
    - skills: Campo que representa las habilidades del candidato.
    - availability: Campo que representa la disponibilidad del candidato.
    - curriculum: Campo que representa el currículum del candidato.
    
    Relaciones:
    - user: Relación con la tabla user.
    - education_list: Relación con la tabla candidate_education.
    - language_list: Relación con la tabla candidate_language.
    - experience_list: Relación con la tabla experience.
    - applied_jobs_list: Relación con la tabla job.
    """

    __tablename__ = CANDIDATE

    user_id: Mapped[UUID] = mapped_column(ForeignKey(f"{USER}.id", name=CandidateConstraint.USER_FK, ondelete="CASCADE"))
    skills: Mapped[list[str]] = mapped_column(ARRAY(String(CandidateStringLen.skills)))
    availability: Mapped[list[WorkSchedule]] = mapped_column(ARRAY(Enum(WorkSchedule)))
    curriculum: Mapped[Optional[bytes]] = deferred(mapped_column(LargeBinary))

    user: Mapped["User"] = relationship(back_populates="candidate", uselist=False, lazy="noload")
    education_list: Mapped[list["CandidateEducation"]] = relationship(back_populates="candidate", lazy="noload")
    language_list: Mapped[list["CandidateLanguage"]] = relationship(back_populates="candidate", lazy="noload")
    experience_list: Mapped[list["Experience"]] = relationship(back_populates="candidate", lazy="noload")
    applied_jobs_list: Mapped[list["JobCandidate"]] = relationship(back_populates="candidate", lazy="noload", order_by=JobCandidate.inscription_date.desc())

    __table_args__ = (
        PrimaryKeyConstraint(user_id, name=CandidateConstraint.CANDIDATE_PK),
        CheckConstraint(
            text(f"check_user_type(user_id, '{UserType.CANDIDATE.value}')"),
            name=CandidateConstraint.USER_NOT_CANDIDATE
        ),
    )

class Company(Base):
    """
    Modelo de la tabla company.

    Esta tabla representa a las empresas de la aplicación.

    Campos:
    - user_id: Campo que representa la clave foránea de la tabla user.
    - tin: Campo que representa el CIF de la empresa.
    - company_name: Campo que representa el nombre de la empresa.

    Relaciones:
    - user: Relación con la tabla user.
    - job_list: Relación con la tabla job.
    """

    __tablename__ = COMPANY

    user_id: Mapped[UUID] = mapped_column(ForeignKey(f"{USER}.id", name=CompanyConstraint.USER_FK, ondelete="CASCADE"))
    _tin: Mapped[str] = mapped_column(String(CompanyStringLen.tin), name="tin")
    _company_name: Mapped[str] = mapped_column(String(CompanyStringLen.company_name), name="company_name")

    user: Mapped["User"] = relationship(back_populates="company", uselist=False, lazy="joined")
    job_list: Mapped[list["Job"]] = relationship(back_populates="company", lazy="noload")

    __table_args__ = (
        PrimaryKeyConstraint(user_id, name=CompanyConstraint.COMPANY_PK),
        UniqueConstraint("tin", name=CompanyConstraint.DUPLICATE_TIN),
        UniqueConstraint("company_name", name=CompanyConstraint.DUPLICATE_COMPANY_NAME),
        CheckConstraint(
            text(f"check_user_type(user_id, '{UserType.COMPANY.value}')"),
            name=CompanyConstraint.USER_NOT_COMPANY
        ),
    )

    @hybrid_property
    def tin(self):
        """Devuelve el CIF de la empresa."""

        return self._tin
    
    @tin.setter
    def tin(self, tin: str):
        """Guarda el CIF de la empresa."""

        self._tin = tin.upper()
    
    @hybrid_property
    def company_name(self):
        """Devuelve el nombre de la empresa."""

        return self._company_name
    
    @company_name.setter
    def company_name(self, company_name: str):
        """Guarda el nombre de la empresa."""

        self._company_name = company_name.lower()


class Language(Base):
    """
    Modelo de la tabla language.

    Esta tabla representa los idiomas de la aplicación.

    Campos:
    - id: Campo que representa la clave primaria de la tabla.
    - name: Campo que representa el nombre del idioma.
    
    Relaciones:
    - candidates_list: Relación con la tabla candidate_language.
    - jobs_list: Relación con la tabla job_language.
    """

    __tablename__ = LANGUAGE

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    _name: Mapped[str] = mapped_column(String(LanguageStringLen.name), name="name")
    
    candidates_list: Mapped[list["CandidateLanguage"]] = relationship(back_populates="language", lazy="noload")
    jobs_list: Mapped[list["JobLanguage"]] = relationship(back_populates="language", lazy="noload")

    __table_args__ = (
        PrimaryKeyConstraint("id", name=LanguageConstraint.LANGUAGE_PK),
        UniqueConstraint("name", name=LanguageConstraint.DUPLICATE_LANGUAGE_NAME),
    )

    @hybrid_property
    def name(self):
        """Devuelve el nombre del idioma."""

        return self._name
    
    @name.setter
    def name(self, name: str):
        """Guarda el nombre del idioma."""

        self._name = name.lower()

class Sector(Base):
    """
    Modelo de la tabla sector.

    Esta tabla representa los sectores de la aplicación.

    Campos:
    - id: Campo que representa la clave primaria de la tabla.
    - category: Campo que representa la categoría del sector.
    - subcategory: Campo que representa la subcategoría del sector.
    
    Relaciones:
    - education_list: Relación con la tabla sector_education.
    - experience_list: Relación con la tabla experience.
    """

    __tablename__ = SECTOR

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    _category: Mapped[str] = mapped_column(String(SectorStringLen.category), index=True, name="category")
    _subcategory: Mapped[str] = mapped_column(String(SectorStringLen.subcategory), name="subcategory")

    education_list: Mapped[list["SectorEducation"]] = relationship(back_populates="sector", lazy="noload")
    experience_list: Mapped[list["Experience"]] = relationship(back_populates="sector", lazy="noload")
    job_list: Mapped[list["Job"]] = relationship(back_populates="sector", lazy="noload")
    
    __table_args__ = (
        PrimaryKeyConstraint("id", name=SectorConstraint.SECTOR_PK),
        UniqueConstraint("category", "subcategory", name=SectorConstraint.DUPLICATE_CATEGORY_SUBCATEGORY),
    )

    @hybrid_property
    def category(self):
        """Devuelve la categoría del sector."""

        return self._category
    
    @category.setter
    def category(self, category: str):
        """Guarda la categoría del sector."""

        self._category = category.lower()

    @hybrid_property
    def subcategory(self):
        """Devuelve la subcategoría del sector."""

        return self._subcategory
    
    @subcategory.setter
    def subcategory(self, subcategory: str):
        """Guarda la subcategoría del sector."""

        self._subcategory = subcategory.lower()

class Experience(Base):
    """
    Modelo de la tabla experience.

    Esta tabla representa la experiencia de los candidatos.

    Campos:
    - id: Campo que representa la clave primaria de la tabla.
    - company_name: Campo que representa el nombre de la empresa.
    - start_date: Campo que representa la fecha de inicio.
    - end_date: Campo que representa la fecha de finalización.
    - job_position: Campo que representa el puesto de trabajo.
    - job_position_description: Campo que representa la descripción del puesto de trabajo.
    - candidate_id: Campo que representa la clave foránea de la tabla candidate.
    - sector_id: Campo que representa la clave foránea de la tabla sector.

    Relaciones:
    - candidate: Relación con la tabla candidate.
    - sector: Relación con la tabla sector.
    """

    __tablename__ = EXPERIENCE

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    _company_name: Mapped[str] = mapped_column(String(ExperienceStringLen.company_name), name="company_name")
    start_date: Mapped[date]
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    _job_position: Mapped[str] = mapped_column(String(ExperienceStringLen.position), name="job_position")
    _job_position_description: Mapped[str] = mapped_column(String(ExperienceStringLen.position_description), name="job_position_description")
    candidate_id: Mapped[UUID] = mapped_column(ForeignKey(f"{CANDIDATE}.user_id", name=ExperienceConstraint.CANDIDATE_FK, ondelete="CASCADE"))
    sector_id: Mapped[UUID] = mapped_column(ForeignKey(f"{SECTOR}.id", name=ExperienceConstraint.SECTOR_FK))

    candidate: Mapped["Candidate"] = relationship(back_populates="experience_list", lazy="noload")
    sector: Mapped["Sector"] = relationship(back_populates="experience_list", lazy="joined")

    __table_args__ = (
        PrimaryKeyConstraint("id", name=ExperienceConstraint.EXPERIENCE_PK),
    )

    @hybrid_property
    def company_name(self):
        """Devuelve el nombre de la empresa."""

        return self._company_name
    
    @company_name.setter
    def company_name(self, company_name: str):
        """Guarda el nombre de la empresa."""

        self._company_name = company_name.lower()

    @hybrid_property
    def job_position(self):
        """Devuelve el puesto de trabajo."""

        return self._job_position
    
    @job_position.setter
    def job_position(self, job_position: str):
        """Guarda el puesto de trabajo."""

        self._job_position = job_position.lower()

    @hybrid_property
    def job_position_description(self):
        """Devuelve la descripción del puesto de trabajo."""

        return self._job_position_description
    
    @job_position_description.setter
    def job_position_description(self, job_position_description: str):
        """Guarda la descripción del puesto de trabajo."""

        self._job_position_description = job_position_description.lower()

class Education(Base):
    """
    Modelo de la tabla education.

    Esta tabla representa la educación de los candidatos.

    Campos:
    - id: Campo que representa la clave primaria de la tabla.
    - qualification: Campo que representa la cualificación.
    - level_id: Campo que representa la clave foránea de la tabla education_level.
    - sector_id: Campo que representa la clave foránea de la tabla sector.
    
    Relaciones:
    - sector: Relación con la tabla sector.
    - level: Relación con la tabla education_level.
    - candidates_list: Relación con la tabla candidate_education.
    - jobs_list: Relación con la tabla job_education.
    """
    
    __tablename__ = EDUCATION

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    _qualification: Mapped[str] = mapped_column(String(EducationStringLen.qualification), name="qualification")
    level_id: Mapped[UUID] = mapped_column(ForeignKey(f"{EDUCATION_LEVEL}.id", name=EducationConstraint.LEVEL_FK))

    sector: Mapped[Optional["SectorEducation"]] = relationship(back_populates="education", lazy="joined", uselist=False)
    level: Mapped["EducationLevel"] = relationship(back_populates="education_list", lazy="joined", order_by="EducationLevel.value")
    candidates_list: Mapped[list["CandidateEducation"]] = relationship(back_populates="education", lazy="noload")
    jobs_list: Mapped[list["JobEducation"]] = relationship(back_populates="education", lazy="noload")

    __table_args__ = (
        PrimaryKeyConstraint("id", name=EducationConstraint.EDUCATION_PK),
        UniqueConstraint("qualification", name=EducationConstraint.DUPLICATE_QUALIFICATION),
    )

    @hybrid_property
    def qualification(self):
        """Devuelve la cualificación."""

        return self._qualification
    
    @qualification.setter
    def qualification(self, qualification: str):
        """Guarda la cualificación."""

        self._qualification = qualification.lower()

class EducationLevel(Base):
    """
    Modelo de la tabla education_level.

    Esta tabla representa los niveles de educación de los candidatos.

    Campos:
    - id: Campo que representa la clave primaria de la tabla.
    - name: Campo que representa el nombre del nivel de educación.
    - value: Campo que representa el valor del nivel de educación.

    Relaciones:
    - education_list: Relación con la tabla education
    """

    __tablename__ = EDUCATION_LEVEL

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    _name: Mapped[str] = mapped_column(String(EducationLevelStringLen.name), name="name")
    value: Mapped[int]

    education_list: Mapped[list["Education"]] = relationship(back_populates="level", lazy="noload")

    __table_args__ = (
        PrimaryKeyConstraint("id", name=EducationLevelConstraint.EDUCATION_LEVEL_PK),
        UniqueConstraint("value", name=EducationLevelConstraint.DUPLICATE_VALUE),
        UniqueConstraint("name", name=EducationLevelConstraint.DUPLICATE_NAME)
    )

    @hybrid_property
    def name(self):
        """Devuelve el nombre del nivel de educación."""

        return self._name
    
    @name.setter
    def name(self, name: str):
        """Guarda el nombre del nivel de educación."""

        self._name = name.lower()

class LanguageLevel(Base):
    """
    Modelo de la tabla language_level.

    Esta tabla representa los niveles de idioma de los candidatos.

    Campos:
    - id: Campo que representa la clave primaria de la tabla.
    - value: Campo que representa el valor del nivel de idioma.
    - name: Campo que representa el nombre del nivel de idioma.

    Relaciones:
    - candidates_language_list: Relación con la tabla candidate_language
    - jobs_language_list: Relación con la tabla job_language.
    """

    __tablename__ = LANGUAGE_LEVEL

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    value: Mapped[int]
    _name: Mapped[str] = mapped_column(String(LanguageLevelStringLen.name), name="name")

    candidates_language_list: Mapped[list["CandidateLanguage"]] = relationship(back_populates="language_level", lazy="noload")
    jobs_language_list: Mapped[list["JobLanguage"]] = relationship(back_populates="language_level", lazy="noload")

    __table_args__ = (
        PrimaryKeyConstraint("id", name=LanguageLevelConstraint.LANGUAGE_LEVEL_PK),
        UniqueConstraint("value", name=LanguageLevelConstraint.DUPLICATE_VALUE),
        UniqueConstraint("name", name=LanguageLevelConstraint.DUPLICATE_NAME)
    )

    @hybrid_property
    def name(self):
        """Devuelve el nombre del nivel de idioma."""

        return self._name
    
    @name.setter
    def name(self, name: str):
        """Guarda el nombre del nivel de idioma."""

        self._name = name.lower()

class Address(Base):
    """
    Modelo de la tabla address.

    Esta tabla representa las direcciones de los usuarios.

    Campos:
    - id: Campo que representa la clave primaria de la tabla.
    - postal_code: Campo que representa el código postal.
    - street: Campo que representa la calle.
    - city: Campo que representa la ciudad.
    - province: Campo que representa la provincia.
    
    Relaciones:
    - users_list: Relación con la tabla user.
    - jobs_list: Relación con la tabla job.
    """

    __tablename__ = ADDRESS

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    postal_code: Mapped[int] = mapped_column(Integer, index=True)
    _street: Mapped[str] = mapped_column(String(AddressStringLen.street), name="street")
    _city: Mapped[str] = mapped_column(String(AddressStringLen.city), name="city")
    _province: Mapped[str] = mapped_column(String(AddressStringLen.province), name="province")

    users_list: Mapped[list["User"]] = relationship(back_populates="address", lazy="noload")
    jobs_list: Mapped[list["Job"]] = relationship(back_populates="address", lazy="noload")

    __table_args__ = (
        PrimaryKeyConstraint("id", name=AddressConstraint.ADDRESS_PK),
        UniqueConstraint(postal_code, name=AddressConstraint.DUPLICATE_POSTAL_CODE),
        UniqueConstraint(postal_code, "city", "province", name=AddressConstraint.DUPLICATE_ADDRESS)
    )

    @hybrid_property
    def street(self):
        """Devuelve la calle."""

        return self._street
    
    @street.setter
    def street(self, street: str):
        """Guarda la calle."""

        self._street = street.lower()

    @hybrid_property
    def city(self):
        """Devuelve la ciudad."""

        return self._city

    @city.setter
    def city(self, city: str):
        """Guarda la ciudad."""

        self._city = city.lower()
    
    @hybrid_property
    def province(self):
        """Devuelve la provincia."""

        return self._province
    
    @province.setter
    def province(self, province: str):
        """Guarda la provincia."""

        self._province = province.lower()


class Job(Base):
    """
    Modelo de la tabla job.

    Esta tabla representa las ofertas de trabajo.

    Campos:
    - id: Campo que representa la clave primaria de la tabla.
    - title: Campo que representa el título de la oferta.
    - description: Campo que representa la descripción de la oferta.
    - required_months_of_experience: Campo que representa los meses de experiencia requeridos.
    - work_schedule: Campo que representa el horario de trabajo.
    - skills: Campo que representa las habilidades requeridas.
    - active: Campo que representa si la oferta está activa.
    - publication_date: Campo que representa la fecha de publicación.
    - address_id: Campo que representa la clave foránea de la tabla address.
    - company_id: Campo que representa la clave foránea de la tabla company.
    - sector_id: Campo que representa la clave foránea de la tabla sector.

    Relaciones:
    - company: Relación con la tabla company.
    - candidates_list: Relación con la tabla candidate.
    - required_education: Relación con la tabla job_education.
    - address: Relación con la tabla address.
    - language_list: Relación con la tabla job_language.
    - sector: Relación con la tabla sector.
    """

    __tablename__ = JOB

    id: Mapped[Optional[UUID]] = mapped_column(SQL_UUID, default=uuid4)
    _title: Mapped[str] = mapped_column(String(JobStringLen.title), name="title")
    _description: Mapped[str] = mapped_column(String(JobStringLen.description), name="description")
    _required_experience: Mapped[timedelta] = mapped_column(INTERVAL, name="required_experience")
    work_schedule: Mapped[WorkSchedule] = mapped_column(Enum(WorkSchedule))
    skills: Mapped[list[str]] = mapped_column(ARRAY(String(JobStringLen.skills)))
    publication_date: Mapped[Optional[date]] = mapped_column(Date, server_default=text("CURRENT_DATE"))
    address_id: Mapped[UUID] = mapped_column(ForeignKey(f"{ADDRESS}.id", name=JobConstraint.ADDRESS_FK))
    company_id: Mapped[UUID] = mapped_column(ForeignKey(f"{COMPANY}.user_id", name=JobConstraint.COMPANY_FK, ondelete="CASCADE"))
    sector_id: Mapped[UUID] = mapped_column(ForeignKey(f"{SECTOR}.id", name=JobConstraint.SECTOR_FK))
    active: Mapped[bool]
    
    company: Mapped["Company"] = relationship(back_populates="job_list", lazy="noload")
    candidates_list: Mapped[list["JobCandidate"]] = relationship(back_populates="job", lazy="noload")
    required_education: Mapped[Optional[JobEducation]] = relationship(back_populates="job", lazy="joined", uselist=False) 
    address: Mapped["Address"] = relationship(back_populates="jobs_list", lazy="joined")
    language_list: Mapped[list["JobLanguage"]] = relationship(back_populates="job", lazy="joined")
    sector: Mapped["Sector"] = relationship(back_populates="job_list", lazy="joined")

    __table_args__ = (
        PrimaryKeyConstraint("id", name=JobConstraint.JOB_PK),
    )

    @hybrid_property
    def title(self):
        """Devuelve el título de la oferta."""

        return self._title
    
    @title.setter
    def title(self, title: str):
        """Guarda el título de la oferta."""

        self._title = title.lower()

    @hybrid_property
    def description(self):
        """Devuelve la descripción de la oferta."""

        return self._description
    
    @description.setter
    def description(self, description: str):
        """Guarda la descripción de la oferta."""

        self._description = description.lower()

    @hybrid_property
    def required_experience(self):
        """Devuelve los meses de experiencia requeridos."""

        return self._required_experience
    
    @required_experience.setter
    def required_experience(self, months_experience: int):
        """Guarda los meses de experiencia requeridos."""

        self._required_experience = timedelta(weeks=months_experience * MONTHS_TO_DAYS_MULTIPLIER)
