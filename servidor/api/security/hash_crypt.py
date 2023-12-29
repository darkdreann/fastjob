from passlib.context import CryptContext
from api.utils.functions.env_config import CONFIG

CRYPT_CONTEXT = CryptContext(schemes=[CONFIG.PASSWORD_CRYPT_SCHEME], deprecated="auto")

def encrypt_string(string: str) -> str:
    """
    Recibe una cadena de texto y devuelve su hash.
    
    Args:
    - string (str): cadena sin encriptar.

    Returns:
    - str: hash de la cadena.
    """

    hashed_string = CRYPT_CONTEXT.hash(string)
    return hashed_string

def verify_string_hash(plain_string: str, hashed_string: str) -> bool:
    """
    Recibe una cadena de texto encriptada y una cadena de texto sin encriptar y devuelve un booleano que indica si la cadena de texto sin encriptar coincide con la contraseña encriptada.
    
    Args:
    - plain_string (str): cadena sin encriptar.
    - hashed_string (str): cadena encriptada.
        
    Returns:
    - bool: True si la cadena de texto coincide con el hash, False si no coincide
    """

    result = CRYPT_CONTEXT.verify(plain_string, hashed_string)
    return result
