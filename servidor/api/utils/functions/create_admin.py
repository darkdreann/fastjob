from typing import Self, Callable, Any
from uuid import UUID, uuid4
from re import match
from sqlalchemy import select
from getpass import getpass
from api.database.connection import get_session
from api.database.database_models.models import User, Address
from api.models.enums.models import UserType
from api.models.functions.validate_functions import validate_password
from api.models.metadata.validators import UserValidators, ValidatePhoneNumbers, AddressValidators
from api.utils.constants.cli_strings import EMPTY_USERNAME, USERNAME_LENGTH_ERROR, EMAIL_ERROR, DUPLICATED_USERNAME, DUPLICATED_EMAIL, PASSWORDS_NOT_MATCH, EMPTY_NAME
from api.utils.constants.cli_strings import EMPTY_SURNAME, PHONES_ERROR, POSTAL_CODE_ERROR, EMPTY_STREET, EMPTY_CITY, EMPTY_PROVINCE, CREATE_ADMIN_MSG, INPUT_USERNAME, INPUT_CITY
from api.utils.constants.cli_strings import INPUT_EMAIL, INPUT_PASSWORD, INPUT_PASSWORD_CONFIRMATION, INPUT_NAME, INPUT_SURNAME, INPUT_PHONES, INPUT_POSTAL_CODE, INPUT_STREET, INPUT_PROVINCE


class NewAdmin:
    """
    Clase que representa un nuevo administrador. Se encarga de pedir los datos necesarios para crear un nuevo administrador y de insertarlos en la base de datos.
    """

    def __init__(self) -> Self:
        """
        Inicializa una instancia de la clase CreateAdmin.

        Returns:
        - Self: Instancia de la clase CreateAdmin.
        """

        self._username: str = None
        self._email: str = None
        self._password: str = None
        self.name: str = None
        self.surname: str = None
        self.phone_numbers: list[int] = None
        self.address_id: UUID = None
        self.address: Address = None
        self.user_type: UserType = UserType.ADMIN


    # decorators
        
    @staticmethod
    def _repeat_if_exception_async(func: Callable) -> Callable:
        """
        Repite la función si se produce un ValueError.
        Para envolver una función asíncrona.

        Args:
        - func (Callable): La función a repetir

        Returns:
        - Callable: La función envuelta que se repetirá si se produce un ValueError
        """
        async def wrapper(*args, **kwargs):
            # repetir hasta que no se produzca un ValueError
            while True:
                try:
                    # ejecutar la función y devolver el resultado si no se produce un ValueError
                    return await func(*args, **kwargs)
                except ValueError as error:
                    # imprimir el error y volver a ejecutar la función
                    print(error)
        return wrapper
    
    @staticmethod
    def _repeat_if_exception(func: Callable) -> Callable:
        """
        Repite la función si se produce un ValueError.

        Args:
        - func (Callable): La función a repetir

        Returns:
        - Callable: La función envuelta que se repetirá si se produce un ValueError
        """
        def wrapper(*args, **kwargs):
            # repetir hasta que no se produzca un ValueError
            while True:
                try:
                    # ejecutar la función y devolver el resultado si no se produce un ValueError
                    return func(*args, **kwargs)
                except ValueError as error:
                    # imprimir el error y volver a ejecutar la función
                    print(error)
        return wrapper

    # Getters y setters

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value):

        # si el valor es None, se lanza un ValueError
        if not value:
            raise ValueError(EMPTY_USERNAME)

        # si el valor no tiene la longitud adecuada, se lanza un ValueError
        if not len(value) >= UserValidators.MIN_LENGTH_USERNAME and not len(value) <= UserValidators.MAX_LENGTH_USERNAME:
            raise ValueError(USERNAME_LENGTH_ERROR.format(MIN=UserValidators.MIN_LENGTH_USERNAME, MAX=UserValidators.MAX_LENGTH_USERNAME))

        self._username = value

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        EMAIL_REGEX = r"^[\w\W]+@[\w\W]+\.[\w\W]+$"

        # si el valor no es un correo electrónico válido, se lanza un ValueError
        if not value or not match(EMAIL_REGEX, value):
            raise ValueError(EMAIL_ERROR)

        self._email = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        # intentar validar que la contraseña cumple los requisitos
        validate_password(value)
        self._password = value

    # Métodos para pedir datos del nuevo administrador

    @_repeat_if_exception_async
    async def _set_username(self) -> None:
        """
        Establece el nombre de usuario para el administrador.

        Solicita al usuario que ingrese un nombre de usuario y verifica si ya existe en la base de datos.
        Si el nombre de usuario ya existe, se genera un ValueError.

        Raises:
        - ValueError: Si el nombre de usuario ya existe en la base de datos.
        """
        # pedir el nombre de usuario
        username = input(INPUT_USERNAME)
        
        # buscar el nombre de usuario en la base de datos 
        user = await self._get_from_db(User.username, User.username == username)

        # si el nombre de usuario ya existe, se lanza un ValueError
        if user:    
            raise ValueError(DUPLICATED_USERNAME)

        self.username = username
 
    @_repeat_if_exception_async
    async def _set_email(self) -> None:
        """
        Establece el correo electrónico del administrador.

        Solicita al usuario que ingrese un correo electrónico y verifica si ya existe en la base de datos.
        Si el correo electrónico ya existe, se genera un ValueError.

        Raises:
        - ValueError: Si el correo electrónico ya existe en la base de datos.
        """
        # pedir el correo electrónico
        email = input(INPUT_EMAIL)

        # buscar el correo electrónico en la base de datos
        user_email = await self._get_from_db(User.email, User.email == email)

        # si el correo electrónico ya existe, se lanza un ValueError
        if user_email:
            raise ValueError(DUPLICATED_EMAIL)

        self.email = email

    @_repeat_if_exception
    def _set_password(self) -> None:
        """
        Establece la contraseña del administrador.

        Solicita al usuario que ingrese una contraseña y la confirme.
        Si las contraseñas no coinciden, se lanza un ValueError.

        Raises:
        - ValueError: Si las contraseñas no coinciden.
        """
        # pedir la contraseña y la confirmación
        password = getpass(INPUT_PASSWORD)
        password_confirm = getpass(INPUT_PASSWORD_CONFIRMATION)

        # si las contraseñas no coinciden, se lanza un ValueError
        if password != password_confirm:
            raise ValueError(PASSWORDS_NOT_MATCH)
    
        self.password = password
     

    def _set_name(self) -> None:
        """
        Establece el nombre y apellidos del administrador.

        Solicita al usuario que ingrese el nombre y los apellidos del administrador.
        Verifica que el nombre no esté vacío y no exceda la longitud máxima permitida.
        Verifica que los apellidos no estén vacíos y no excedan la longitud máxima permitida.
        """
        CHECK_NAME: Callable[[str, int], bool] = lambda string, length: string and len(string) <= length

        # pedir el nombre del administrador mientras no cumpla los requisitos
        while CHECK_NAME(name := input(INPUT_NAME), UserValidators.MAX_LENGTH_NAME):
            print(EMPTY_NAME)
        self.name = name

        # pedir los apellidos del administrador mientras no cumplan los requisitos
        while CHECK_NAME(surname := input(INPUT_SURNAME), UserValidators.MAX_LENGTH_SURNAME):
            print(EMPTY_SURNAME)
        self.surname = surname

    def _set_phone_numbers(self) -> None:
        """
        Establece los números de teléfono del administrador.

        Solicita al usuario que ingrese los números de teléfono separados por coma.
        Verifica que los números ingresados sean válidos y los asigna a la variable phone_numbers.
        """
        CHECK_NUMBER: Callable[[str], bool] = lambda number: number.isdigit() and len(number) == ValidatePhoneNumbers.PHONE_NUMBERS_LENGTH
        
        while True:
            # pedir los números de teléfono separados por coma
            phone_numbers_str = input(INPUT_PHONES).split(",")
            # convertir los números de teléfono a enteros
            phone_numbers_int = [int(number) for number in phone_numbers_str if CHECK_NUMBER(number)]

            # si se han introducido números de teléfono válidos, se asignan a la variable phone_numbers y termina la función
            if len(phone_numbers_int) == len(phone_numbers_str):
                self.phone_numbers = phone_numbers_int
                return
            
            # si no se han introducido números de teléfono válidos, se vuelve a pedir los números de teléfono
            print(PHONES_ERROR)

    async def _set_address(self) -> None:
        """
        Establece la dirección del administrador.

        Verifica y solicita al usuario que ingrese un código postal válido.
        Si el código postal ya existe en la base de datos, asigna el ID de la dirección existente al administrador.
        Si el código postal no existe en la base de datos, crea una nueva dirección y asigna su ID al administrador.
        """
        CHECK_POSTAL_CODE: Callable[[int], bool] = lambda postal_code: postal_code > AddressValidators.MIN_POSTAL_CODE and postal_code < AddressValidators.MAX_POSTAL_CODE
        
        # pedir el código postal mientras no cumpla los requisitos
        while not CHECK_POSTAL_CODE(postal_code := NewAdmin._int_input(INPUT_POSTAL_CODE)):
            print(POSTAL_CODE_ERROR)

        # buscar el código postal en la base de datos
        address_id = await self._get_from_db(Address.id, Address.postal_code == postal_code)
        
        # si el código postal ya existe, se asigna el ID de la dirección existente al administrador
        if address_id:
            self.address_id = address_id
        
        # si el código postal no existe, se crea una nueva dirección y se asigna su ID al administrador
        else:
            self._create_address(postal_code)

    def _create_address(self, postal_code: int) -> None:
        """
        Crea una dirección para el administrador.

        Args:
        - postal_code (int): El código postal de la dirección.
        """
        # pedir la calle, la ciudad y la provincia mientras no cumplan los requisitos
        while (street := input(INPUT_STREET)) == "":
            print(EMPTY_STREET)
        
        # pedir la ciudad y la provincia mientras no cumplan los requisitos
        while (city := input(INPUT_CITY)) == "":
            print(EMPTY_CITY)
        
        # pedir la provincia mientras no cumpla los requisitos
        while (province := input(INPUT_PROVINCE)) == "":
            print(EMPTY_PROVINCE)

        # crear una nueva dirección
        new_address = Address(
            id = uuid4(),
            postal_code = postal_code,
            street = street,
            city = city,
            province = province
        )

        # asignar la dirección al nuevo administrador
        self.address = new_address

    def _get_admin_dict(self) -> dict:
        """
        Devuelve un diccionario con los atributos del objeto que no son None.

        Returns:
        - dict: Diccionario con los atributos del objeto.
        """
        return {key.lstrip("_"): value for key, value in vars(self).items() if value is not None}
    
    async def _db_commit(self) -> None:
        """
        Realiza la confirmación de los cambios en la base de datos.

        Raises:
        - Exception: Si ocurre algún error durante la confirmación, se realiza un rollback y se lanza la excepción.
        """
        async for session in get_session():
            try:
                # creamos un nuevo usuario con los datos del administrador
                admin_user = User(**self._get_admin_dict())
                # añadimos el usuario a la sesión y hacemos commit
                session.add(admin_user)
                await session.commit()
            except Exception as error:
                # si ocurre algún error, hacemos rollback y lanzamos la excepción
                await session.rollback()
                raise error

    # classmethods

    @classmethod
    async def create_admin(cls) -> None:
        """
        Crea un nuevo administrador y lo inserta en la base de datos.
        """

        NEW_ADMIN = cls()

        print(CREATE_ADMIN_MSG)
        await NEW_ADMIN._set_username()
        await NEW_ADMIN._set_email()
        NEW_ADMIN._set_password()
        NEW_ADMIN._set_name()
        NEW_ADMIN._set_phone_numbers()
        await NEW_ADMIN._set_address()

        await NEW_ADMIN._db_commit()
        
        

    # staticmethods

    @staticmethod
    def _int_input(msg: str) -> int:
        """
        Convierte la entrada del usuario en un entero.

        Args:
        - msg (str): El mensaje que se muestra al usuario para pedir la entrada.

        Return:
        - int: El valor entero ingresado por el usuario. Si la entrada no es un número entero válido, se retorna 0.
        """
        try:
            return int(input(msg))
        except ValueError:
            return 0
        
    @staticmethod
    async def _get_from_db(table: Any, clause: bool) -> Any:
        """
        Obtiene un registro de la base de datos según la tabla y la cláusula especificadas.

        Args:
        - table (Any): La tabla de la base de datos.
        - clause (bool): La cláusula de búsqueda.

        Returns:
        - Any: El registro obtenido de la base de datos.
        """
        async for session in get_session():
            # creamos la query
            query = select(table).where(clause)
            # ejecutamos la query y obtenemos el resultado
            result = await session.execute(query)
            record = result.scalar_one_or_none()

            return record
        
    
            

        


        

