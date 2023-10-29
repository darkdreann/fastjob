ENV_FILE_NOT_FOUND = "File .env not found"
ENV_UNEXPECTED_ERROR = "Error: Something went wrong reading .env file:\n {exc}"
ENV_VARS_NOT_FOUND = "Error: environment variables not found: {vars}"

DATABASE_ERROR = "Error: Database error: {exc}."
TABLES_AND_FUNCTIONS_FAILED = "Error: Tables and functions creation failed\n {exc}"	

UNKNOWN_ERROR = "Error: Something went wrong server stoped. Please check the logs for more information."

USER_NOT_FOUND = "Error: User {resource_id} requested not found by user {user_id}"

PERMISSION_USER_NOT_FOUND = "Error: Permission denied user not found"
PERMISSION_DENIED = "Error: Permission denied user {user_id} not allowed to access resource {resource_id}"

INVALID_TOKEN = "Error: Invalid token provided:\n {exc}"

INVALID_CREDENTIALS = "Error: Could not validate credentials for {username}"

INVALID_PARAMS_ERROR = "Error: Invalid params provided:\n {exc}"

LOG_FOLDER_CREATE_PERMISSION_DENIED = "Error: Permission denied creating log folder"

LOG_FORMAT_ERROR = "Error: Cannot format log message:\n {exc}"

ERROR_RESPONSE_UNEXPECTED_ERROR = "Error: Something went wrong. Please try again later."

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


