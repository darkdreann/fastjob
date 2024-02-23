# FastJob Android

Esta aplicación Android está diseñada para brindar a los usuarios una interfaz intuitiva y eficiente para interactuar con una API REST. Permite a los usuarios acceder y utilizar los diversos servicios proporcionados por la API de manera conveniente desde sus dispositivos móviles.

## Índice

- [Requisitos](#Requisitos)
- [Instrucciones](#Instrucciones-de-uso)
- [Estructura del proyecto](#Estructura-del-proyecto)

## Requisitos

Para disfrutar plenamente de todas las funcionalidades de esta aplicación, asegúrate de cumplir con los siguientes requisitos mínimos:

- Dispositivo con sistema operativo Android versión 26 o superior.
- Acceso a Internet activo para aprovechar al máximo las capacidades de conexión y utilizar los servicios de la aplicación de manera efectiva.

## Instrucciones de uso

Para acceder a nuestra aplicación, solo necesitas instalar el archivo APK en tu dispositivo Android. Una vez instalada, podrás comenzar a utilizar todas las funciones disponibles sin complicaciones adicionales.

## Estructura del proyecto

- **auth**: Contiene los archivos Kotlin responsables de la gestión de la autenticación en la aplicación.
- **models**: Alberga los archivos Kotlin que contienen los modelos de datos utilizados en la aplicación.
    - **interfaces**: Aloja las interfaces utilizadas en los modelos de la aplicación.
    - **serializer**: Incluye los serializadores utilizados para convertir las clases a formato JSON para los servicios de la API.

- **network**: Contiene los archivos Kotlin responsables de la conexión con la API.

- **services**: Contiene los archivos Kotlin con las definiciones para las peticiones a los endpoints de la API.

- **ui**: Almacena los archivos Kotlin relacionados con la interfaz de usuario (UI) de la aplicación.
    - **componets**: Agrupa los componentes de la aplicación.
        - **basic**: Contiene los componentes más básicos de la aplicación.
        - **candidate**: Engloba los componentes relacionados con los candidatos dentro de la aplicación.
        - **company**: Engloba los componentes relacionados con las empresas dentro de la aplicación.
        - **form**: Agrupa los componentes que actúan como formularios dentro de la aplicación.
        - **job**: Alberga los componentes relacionados con las ofertas dentro de la aplicación.
        - **navigation**: Contiene el componente encargado de la navegación entre pantallas dentro de la aplicación.
        - **profile**: Contiene los componentes que representan los perfiles de usuarios dentro de la aplicación.
    - **effects**: Almacena los diferentes efectos personalizados utilizados en la aplicación.
    - **enums**: contiene los enums utilizados en los componentes o viewmodels de la aplicación.
    - **functions**: Contiene funciones de utilidad para la aplicación.
        - **keywords**: Engloba funciones de utilidad relacionadas con las búsquedas de palabras clave dentro de la aplicación.
    - **navigation**: Contiene una clase sellada que enumera las diferentes pantallas de la aplicación.
    - **screens**: Agrupa las diferentes pantallas de la aplicación.
    - **theme**: Contiene los datos relacionados con los temas de la aplicación.
    - **viewmodels**: Incluye los viewmodels de la aplicación.
        - **candidate**: Incorpora los viewmodels relacionados específicamente con las pantallas de candidatos en la aplicación.
        - **company**: Agrupa los viewmodels relacionados específicamente con las pantallas de empresas en la aplicación.
        - **interfaces**: Contiene las interfaces utilizadas en los viewmodels de la aplicación.
        - **job**: Contiene los viewmodels relacionados específicamente con las pantallas de ofertas en la aplicación.
        - **login**: Contiene los viewmodels relacionados específicamente con la pantalla de inicio de sesión en la aplicación.
        - **profile**: Contiene los viewmodels asociados directamente con los perfiles de usuario en la aplicación.
        - **search**: Alberga los viewmodels vinculados con las búsquedas en la aplicación.
        - **user**: Engloba los viewmodels relacionados con los usuarios en la aplicación.

- **MainActivity.kt**: La actividad principal de la aplicación.