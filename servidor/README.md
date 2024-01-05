# FastJobAPI

Esta API Restful asume la responsabilidad de gestionar la autenticación de usuarios y llevar a cabo las operaciones CRUD dentro del ámbito de la API. Facilita la interacción de las aplicaciones frontend con los datos mediante los endpoints específicos. Además, cuenta con un sistema de registros (logs) que posibilita que la API registre tanto los accesos a los endpoints como los posibles errores que puedan surgir en su ejecución.

## Índice

- [Requisitos](#Requisitos)
- [Instrucciones](#Instrucciones-de-uso)
- [Archivos ENV](#Archivos-ENV)
- [Archivo JSON DEV](#Archivo-JSON-DEV)
- [Estructura del proyecto](#Estructura-del-proyecto)

## Requisitos

Para implementar el servidor de esta API, se emplea Gunicorn como gestor de procesos, estableciendo comunicación con los Workers de Uvicorn. Como consecuencia de esta configuración, no es factible desplegar la API en un entorno Windows. No obstante, se ofrece la alternativa de implementarla en un contenedor Docker, requiriendo, para ello, la instalación previa de Docker en el sistema correspondiente.

## Instrucciones de uso

La API incorpora el script "manage.py" con el propósito de facilitar tanto la implementación como la creación de un contenedor Docker. Asimismo, posibilita la creación de un administrador desde la interfaz de línea de comandos (CLI).

Los argumentos contemplados para el script son los siguientes:
- runserver: Habilita la ejecución del servidor asociado a la API.
- createadmin: Habilita la creación de un administrador en la interfaz de línea de comandos (CLI).
- dockerbuild: Facilita la creación de contenedores Docker tanto para entornos de desarrollo como de producción.

> [!WARNING]
> Antes de utilizar la API, es necesario generar los archivos de entorno (env) según se especifica en el próximo apartado.

## Archivos ENV

Para la ejecución de la API, se requiere la creación de un archivo .env. La API brinda la opción de contar con dos archivos env:

- .env: Archivo .env diseñado para su implementación en entornos de producción.
- .env.dev: Archivo .env diseñado para su implementación en entornos de desarrollo.

Ambos archivos .env requieren las siguientes variables de entorno:

- SECRET_KEY: Clave secreta utilizada para la autenticación de la API.
- ACCESS_TOKEN_EXPIRE_MINUTES: Duración del tiempo durante el cual los tokens de la API permanecen válidos antes de su expiración.
- ALGORITHM: Algoritmo empleado en el proceso de autenticación.
- TOKEN_TYPE: Tipo de token empleado por la API.
- TOKEN_URL: Ruta donde se aplica el proceso de autenticación.
- PASSWORD_CRYPT_SCHEME: Algoritmo empleado en el proceso de hash de las contraseñas.

> Estas variables determinan los parámetros de seguridad de la API.

- LOGS_PATH: Directorio destinado al almacenamiento de los diversos registros generados.
- APP_LOG_FOLDER: Directorio de almacenamiento para los diversos registros generados por la API.
- LOG_FILE_INFO: Archivo destinado al almacenamiento de los registros informativos de la API.
- LOG_FILE_ERROR: Archivo destinado al almacenamiento de los registros de errores de la API.
- CONFIG_FILE_PATH: Ubicación destinada al almacenamiento del archivo de configuración de los registros de la API.
- APP_LOGGING_CONFIG_FILE: Archivo que contiene la configuración de los registros de la API.

> Estas variables definen los parámetros del sistema de registros (logs) de la API.

- SMTP_SERVER: Dirección IP del servidor SMTP.
- SMTP_PORT: Número de puerto del servidor SMTP.
- SMTP_EMAIL: Correo electrónico.
- SMTP_PASSWORD: Contraseña del correo electrónico.
- EMAIL_TO_SEND: Dirección de correo electrónico a la cual se enviará el mensaje.
- SUBJECT: Asunto del mensaje a ser enviado.

> Estas variables establecen los parámetros del correo electrónico utilizado en el logger SMTP en caso de producirse un error crítico en la API.

- SERVER_IP: Dirección IP del servidor. Se recomienda establecer en 0.0.0.0 en caso de emplear Docker.
- SERVER_PORT: Número de puerto del servidor.
- SERVER_WORKERS: Número de procesos del servidor. No es necesario en entornos de desarrollo.

> Estas variables definen la configuración del servidor. En entornos de desarrollo donde no se utiliza Docker, estas variables podrían no ser requeridas.

- POSTGRES_USER: Nombre de usuario de PostgreSQL con privilegios de superusuario.
- POSTGRES_PASSWORD: Clave del usuario de PostgreSQL.
- POSTGRES_DB: Nombre de la base de datos predeterminada en PostgreSQL.

> Estas variables configuran los parámetros del contenedor Docker de PostgreSQL. Su especificación no es requerida en caso de prescindir del uso de Docker.

- DATABASE_IP: Dirección IP de la base de datos. En el caso de utilizar Docker, sería el nombre del contenedor.
- DATABASE_PORT: Número de puerto de la base de datos.
- DATABASE_NAME: Nombre de la base de datos utilizada por la API.
- DATABASE_USERNAME: Nombre de usuario encargado de la gestión de la base de datos de la API.
- DATABASE_PASSWORD: Contraseña del usuario responsable de la administración de la base de datos de la API.
- POOL_SIZE: Cantidad de conexiones activas en la API destinadas a la interacción con la base de datos.
- MAX_OVERFLOW: Número temporal de conexiones adicionales que pueden crearse más allá de la capacidad máxima para atender las solicitudes.

> Estas variables establecen la configuración de la conexión de la API con la base de datos.

Variables exclusivas del archivo .env:

- GUNICORN_LOG_LEVEL: Nivel de registros (logs) de Gunicorn.
- GUNICORN_LOG_FOLDER: Directorio destinado al almacenamiento de los archivos de registro (logs) de Gunicorn.
- GUNICORN_ACCESS_LOG: Archivo donde se registran los registros de acceso de Gunicorn.
- GUNICORN_ERROR_LOG: Archivo designado para el registro de errores en Gunicorn.

> Estas variables establecen la configuración de registros (logs) de Gunicorn.

Variables exclusivas del archivo .env.dev:

- PGADMIN_DEFAULT_EMAIL: Dirección de correo electrónico para el usuario de PgAdmin.
- PGADMIN_DEFAULT_PASSWORD: Clave del usuario de PgAdmin.
- PGADMIN_PORT: Puerto utilizado por pgadmin.

> Estas variables definen la configuración de PgAdmin. Su especificación no es necesaria en ausencia de la utilización de Docker.

- TEST_DATA_JSON_PATH: Nombre del archivo JSON que facilita la inserción de datos de prueba para el desarrollo.

> Esta variable posibilita la selección del nombre para el archivo JSON.

> [!NOTE]
> En la sección siguiente se describe la estructura que debe seguir el archivo JSON.

## Archivo JSON DEV

El archivo JSON facilita la inserción automática de datos de prueba en el modo de desarrollo, permitiendo así simplificar la realización de pruebas.

La estructura básica es la siguiente:

```JSON
{   
    "Address":[

    ],
    "User":[

    ]
}
```

Los modelos aceptados son:

1. Address
2. User
3. Candidate
4. Company
5. Sector
6. EducationLevel
7. Education
8. SectorEducation
9. CandidateEducation
10. Experience
11. Language
12. LanguageLevel
13. CandidateLanguage
14. Job
15. JobEducation
16. JobLanguage

> [!IMPORTANT]
> Se recomienda adherirse al orden indicado para garantizar un funcionamiento correcto.

La estructura del modelo "Address" es la siguiente:

```JSON
"Address":
    [
        {   
            "id":"UUID",
            "street":"CALLE",
            "province":"PROVINCIA",
            "city":"CIUDAD",
            "postal_code": 15000 // código postal
        }
    ]
```

La estructura del modelo "User" es la siguiente:

```JSON
    "User":
    [
        {   
            "id":"UUID",
            "username":"NOMBRE DE USUARIO",
            "password":"CONTRASEÑA",
            "user_type":"TIPO DE USUARIO", // ADMIN - CANDIDATE - COMPANY
            "email":"EMAIL",
            "phone_numbers":[612094756], //Números de teléfono 
            "name":"NOMBRE",
            "surname":"APELLIDO",
            "address_id":"UUID" // UUID de una dirección creada
        }
    ]
```

La estructura del modelo "Candidate" es la siguiente:

```JSON
    "Candidate":[
        {
            "user_id":"UUID", // UUID de un usuario tipo CANDIDATE creado
            "skills":["HABILIDAD1", "HABILIDAD2"],
            "availability":["DISPONIBILIDAD1", "DISPONIBILIDAD2"]
            // FULL-TIME - PART-TIME - MORNING - AFTERNOON - DAY - NIGHT - FLEXTIME - REMOTE-WORK - ANY
        }
    ]
```

La estructura del modelo "Company" es la siguiente:

```JSON
    "Company":[
        {
            "user_id":"UUID", // UUID de un usuario tipo COMPANY creado
            "company_name":"NOMBRE EMPRESA",
            "tin":"CIF"
        }
    ]
```

La estructura del modelo "Sector" es la siguiente:

```JSON
    "Sector":[
        {
            "id":"UUID",
            "category":"CATEGORÍA SECTOR", // IT
            "subcategory":"SUBCATEGORÍA SECTOR" // DEVELOPER
        }
    ]
```

La estructura del modelo "EducationLevel" es la siguiente:

```JSON
        {
            "id":"UUID",
            "name":"NOMBRE DEL NIVEL", // GRADO SUPERIOR
            "value":3 // Valor númerico del nivel
        }
```

La estructura del modelo "Education" es la siguiente:

```JSON
  "Education":[
        {
            "id":"UUID",
            "qualification":"NOMBRE TITULO", // Desarrollo de Aplicaciones Multiplataforma
            "level_id":"UUID" // UUID de un nivel de formación creado
        }
    ]
```

La estructura del modelo "SectorEducation" es la siguiente:

```JSON
    "SectorEducation":[
        {
            "education_id":"UUID", // UUID de una formación creada
            "sector_id":"UUID" // UUID de un sector creado
        }
    ]
```

La estructura del modelo "CandidateEducation" es la siguiente:

```JSON
    "CandidateEducation":[
        {
            "candidate_id":"UUID", // UUID de un candidato creado
            "education_id":"UUID", // UUID de una formación creada
            "completion_date": {
                "year": 2019, // Año de finalización de la formación
                "month": 6, // Mes de finalización de la formación
                "day": 1 // Día de finalización de la formación
            }
        }
    ]
```

La estructura del modelo "Experience" es la siguiente:

```JSON
    "Experience":[
        {
            "id": "UUID",
            "company_name": "NOMBRE EMPRESA TRABAJADA",
            "start_date": {
                "year": 2019, // Año de inicio de la experiencia
                "month": 6, // Año de inicio de la experiencia
                "day": 1 // Año de inicio de la experiencia
            },
            "job_position":"POSICION", // Desarrollador
            "job_position_description": "DESCRIPCION", // Descripción del puesto
            "candidate_id": "UUID", // UUID de un candidato creado
            "sector_id": "UUID" // UUID de un sector creado
        },
        {
            "id": "UUID",
            "company_name": "NOMBRE EMPRESA TRABAJADA",
            "start_date": {
                "year": 2019, // Año de inicio de la experiencia
                "month": 6, // Mes de inicio de la experiencia
                "day": 1 // Día de inicio de la experiencia
            },
            "end_date": {
                "year": 2023, // Año de finalización de la experiencia
                "month": 1, // Mes de finalización de la experiencia
                "day": 1 // Día de finalización de la experiencia
            },
            // La fecha de finalización no es obligatoria
            "job_position":"POSICION", // Desarrollador
            "job_position_description": "DESCRIPCION", // Descripción del puesto
            "candidate_id": "UUID", // UUID de un candidato creado
            "sector_id": "UUID" // UUID de un sector creado
        }
    ]
```

La estructura del modelo "Language" es la siguiente:

```JSON
    "Language":[
        {
            "id":"UUID",
            "name":"NOMBRE IDIOMA" // Español
        }
    ]
```

La estructura del modelo "LanguageLevel" es la siguiente:

```JSON
    "LanguageLevel":[
        {
            "id":"UUID",
            "name":"NOMBRE NIVEL", // B1
            "value":1 // Valor númerico del nivel
        }
    ]
```

La estructura del modelo "CandidateLanguage" es la siguiente:

```JSON
    "CandidateLanguage":[
        {
            "candidate_id":"UUID", // UUID de un candidato creado
            "language_id":"UUID", // UUID de un idioma crado
            "language_level_id":"UUID" // UUID de un nivel de idioma creado
        }
    ]
```

La estructura del modelo "Job" es la siguiente:

```JSON
    "Job":[
        {
            "id":"UUID",
            "title":"TITULO OFERTA", // Programador Java
            "description":"DESCRIPCION", // Descripción del puesto
            "required_experience":25, // Meses de experiencia requerida
            "work_schedule":"FULL-TIME", // Disponibilidad requerida
            // FULL-TIME - PART-TIME - MORNING - AFTERNOON - DAY - NIGHT - FLEXTIME - REMOTE-WORK - ANY
            "skills":["HABILIDAD1", "HABILIDAD2"], // Habilidades requeridas en la oferta
            "active":true, // si la oferta esta abierta o cerrada
            "address_id":"UUID", // UUID de una dirección creada
            "company_id":"UUID", // UUID de una empresa creada
            "sector_id":"UUID", // UUID de un sector creado
        }
    ]
```

La estructura del modelo "JobEducation" es la siguiente:

```JSON
    "JobEducation":[
        {
            "job_id":"UUID", // UUID de una oferta de trabajo creada
            "education_id":"UUID", // UUID de una formación creada
        }
    ]
```

La estructura del modelo "JobLanguage" es la siguiente:

```JSON
    "JobLanguage":[
        {
            "job_id":"UUID", // UUID de una oferta de trabajo creada
            "language_id":"UUID", // UUID de un idioma creado
            "language_level_id":"UUID", // UUID de un nivel de idioma creado
        }
    ]
```

> [!IMPORTANT]
> Se sugiere la inserción de un mínimo de cuatro registros por cada modelo para lograr pruebas óptimas.

## Estructura del proyecto

- **api**: Contiene todos los módulos de la API.
    - **database**: Módulo encargado de la conexión y los modelos de la base de datos.
        - **connection.py**: Contiene la conexión a la base de datos.
        - **database_functions.py**: Contiene funciones que deben ser creadas por la base de datos.
        - **database_models**: Módulo que alberga los modelos de la base de datos.
        - **metadata**: Módulo que almacena información referente a los modelos.
            - **constraint_name.py**: Almacena los nombres de las restricciones (constraints) de las tablas.
            - **string_length.py**: Almacena los valores máximos de las columnas varchar de las tablas.
            - **table_name.py**: Almacena los nombres de las tablas.

    - **loggs**: Módulo encargado de los registros (logs) de la API.
        - **load_config.py**: Contiene la lógica para cargar el archivo YAML con la configuración de registro (logging).
        - **loggers**: Realiza la carga de la configuración y obtiene los registradores (loggers) de información y errores para su utilización en la API.
        - **logging_config.yml**: Archivo YAML que alberga la configuración de registros (logs).

    - **models**: Módulo que incorpora los modelos empleados en los puntos finales (endpoints) para la entrada y salida de datos.
        - **base_models.py**: Comprende los modelos fundamentales, siendo estos la base de herencia para los demás modelos.
        - **create_models.py**: Engloba los modelos utilizados para la creación de registros, los cuales son empleados para la entrada de datos.
        - **update_models.py**: Incorpora los modelos empleados para la actualización de registros, los cuales también son utilizados para la entrada de datos.
        - **partial_update_models.py**: Incluye los modelos destinados a la actualización de registros, con la particularidad de que, a diferencia de update_models, permite enviar solo los campos requeridos. Se utiliza para la entrada de datos.
        - **enums**: Módulo que alberga enumeraciones (enums) empleadas en la API.
            - **endpoints.py**: Incluye enumeraciones (enums) que son utilizadas en los puntos finales (endpoints) de la API.
            - **models.py**: Incorpora enumeraciones (enums) que son empleadas en los diversos modelos de la API.
        - **funtions**: Módulo que incluye funciones utilizadas por los modelos.
            - **validate_functions.py**: Incorpora funciones de validación utilizadas por los modelos.
        - **metadata**: Módulo que alberga información acerca de los modelos.
            - **constants.py**: Incluye valores constantes destinados a los modelos.
            - **descriptions.py**: Almacena descripciones de los campos de los modelos utilizados para la documentación.
            - **validators.py**: Incluye valores destinados a la validación de los campos de los modelos.
    
    - **routers**: Módulo que encapsula los endpoints utilizados en la API.
        - **address.py**: Contiene los endpoints que gestionan la dirección.
        - **candidate_education.py**: Engloba los endpoints que administran la relación entre candidato y su formación.
        - **candidate_language.py**: Contiene los endpoints que manejan la relación entre candidatos e idiomas.\
        - **candidate.py**: Engloba los endpoints encargados de gestionar los candidatos.
        - **company.py**: Aloja los endpoints encargados de gestionar las empresas.
        - **education.py**: Engloba los endpoints destinados a gestionar las formaciones.
        - **experience.py**: Engloba los endpoints encargados de gestionar las experiencias laborales de los candidatos.
        - **job_candidate.py**: Aloja los endpoints que gestionan la relación entre candidatos y ofertas laborales.
        - **job.py**: Aloja los endpoints encargados de gestionar las ofertas laborales.
        - **language.py**: Engloba los endpoints dedicados a gestionar los idiomas.
        - **sector.py**: Engloba los endpoints destinados a gestionar los sectores.
        - **user.py**: Aloja los endpoints encargados de gestionar los usuarios y el proceso de inicio de sesión.

    - **security**: Módulo encargado de la seguridad de la API.
        - **hash_crypt.py**: Se encarga de realizar el hash y la verificación de las contraseñas.
        - **permissions.py**: Incluye la lógica de los permisos necesarios para los endpoints.
        - **security.py**: Incorpora la lógica para la creación, verificación y decodificación de los tokens.
    
    - **tests**: Módulo que incorpora la lógica de pruebas de la API.
        - **endpoint_tests**: Aloja las pruebas correspondientes a los diversos endpoints.
        - **test_utils**: Módulo que alberga funciones destinadas a las pruebas.
            - **data_json.py**: Se encarga de obtener los datos almacenados en el archivo JSON.
            - **db_manage_tests.py**: Incluye la lógica para almacenar la información obtenida del archivo JSON en la base de datos.
            - **result_tests.py**: Incorpora la lógica para verificar la corrección de los resultados de las pruebas de los endpoints.
    
    - **utils**: Módulo que alberga diversas utilidades destinadas a la API.
        - **constants**: Módulo que alberga diversas constantes utilizadas en la API.
            - **cli_strings.py**: Incorpora cadenas de texto utilizadas en las distintas interfaces de línea de comandos (CLI) de la API.
            - **endpoint_params.py**: Incluye diversos parámetros utilizados en la documentación de los endpoints.
            - **error_strings.py**: Incorpora cadenas de texto de error empleadas en los endpoints.
            - **http_exceptions.py**: Incluye respuestas HTTP para diversas excepciones que podrían surgir en la API.
            - **info_strings.py**: Alberga cadenas de texto informativas utilizadas en los endpoints.
        - **functions**: Módulo que incorpora funciones de utilidad para la API.
            - **candidate_filter.py**: Se encarga de la lógica para filtrar usuarios mediante parámetros.
            - **create_admin.py**: Permite la creación de un administrador mediante la interfaz de línea de comandos (CLI).
            - **database_utils.py**: Incluye lógica para la inserción o recuperación de datos de la base de datos.
            - **docker_build.py**: Facilita la creación de contenedores Docker mediante una interfaz de línea de comandos (CLI) guiada.
            - **env_config.py**: Recupera las variables de entorno y genera un objeto con dichas variables.
            - **exception_handlers.py**: Lógica encargada de gestionar las excepciones y proporcionar una respuesta al usuario.
            - **job_filter.py**: Se encarga de la lógica que permite filtrar las ofertas de trabajo mediante parámetros.
            - **management_utils.py**: Administra los registros (logs) de la aplicación.
            - **models_utils.py**: Funciones de utilidad que administran modelos destinados a los endpoints.
            - **run_server.py**: Facilita la inicialización del servidor de la API.
        - **exceptions.py**: Contiene diversas excepciones utilizadas en la API.
    
    - **main.py**: Archivo principal que inicia la ejecución de la API.
- **docker_files**: Alberga archivos para la generación de contenedores Docker.
    - **create_db.sh**: Script encargado de facilitar la creación de la base de datos y su respectivo usuario para la API.
    - **Dockerfile**: Archivo para la creación de la imagen Docker destinada a entornos de producción.
    - **Dockerfile.dev**: Archivo para la creación de la imagen Docker destinada al entorno de desarrollo.
- **docker-compose.dev.yml**: Archivo YAML con la especificación de los contenedores Docker para el entorno de desarrollo.
- **docker-compose.yml**: Archivo YAML con la configuración de los contenedores Docker para el entorno de producción.
- **manage.py**: Script que simplifica la inicialización del servidor, la creación de contenedores Docker, y también posibilita la creación de un administrador a través de la interfaz de línea de comandos (CLI).
- **requirements.txt**: Incluye las dependencias de la API.