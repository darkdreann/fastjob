ENV_FILE_NOT_FOUND = "File .env not found"
ENV_UNEXPECTED_ERROR = "Error: Something went wrong reading .env file:\n {exc}"

DATABASE_ERROR = "Error: Database error: {exc}."
TABLES_AND_FUNCTIONS_FAILED = "Error: Tables and functions creation failed\n {exc}"	

UNKNOWN_QUERY_ERROR = "Error: Something went wrong in query:\n {exc}"

RESOURCE_NOT_FOUND = "Error: Resource {resource_id} type {resource_type} requested not found"

RESOURCES_NOT_FOUND = "Error: Resources type {resource_type} not found query:\n {query}"

PERMISSION_USER_NOT_FOUND = "Error: Permission denied user not found"

PERMISSION_DENIED = "Error: Permission denied user {user_id} not allowed to access resource {resource}"

INVALID_TOKEN = "Error: Invalid token provided:\n {exc}"

INVALID_CREDENTIALS = "Error: Could not validate credentials for {username}"

INVALID_PARAMS_ERROR = "Error: Invalid params provided:\n {exc}"

LOG_FOLDER_CREATE_PERMISSION_DENIED = "Error: Permission denied creating log folder"

LOG_FORMAT_ERROR = "Error: Cannot format log message:\n {exc}"

ERROR_RESPONSE_UNEXPECTED_ERROR = "Error: Something went wrong. Please try again later."

SECTOR_GET_PARAMS = "category_name and only_categories params cannot be used at the same time."

INVALID_EXTRA_FIELDS = "Error: Extra fields params not valid:\n {field}"


# EXCEPTION HANDLERS MESSAGES
LOG_INVALID_PARAMS = """
Invalid params:
  params: {params},
  Request:
    url: {url},
    method: {method}"""

LOG_UNEXPECTED_ERROR = """
Error: {exc},
Request:
  url: {url},
  method: {method}"""


