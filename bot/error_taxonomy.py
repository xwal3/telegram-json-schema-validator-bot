# I Can Refactor it much better and make it class based and add another validators like haluciantion and others

"""
from jsonschema import validate, ValidationError
from telegram import Update
from telegram.ext import ContextTypes

async def validate_json_payload(update: Update, context: ContextTypes.DEFAULT_TYPE, schema: dict, data: dict):

    try:
        validate(instance=data, schema=schema)
        await update.message.reply_text("✅ Validation successful! The JSON data conforms to the schema.")
    except ValidationError as e:
        error_taxonomy = "Validation Error"
        if e.validator == "required":
            error_taxonomy = "Missing Required Parameter"
        elif e.validator == "type":
            error_taxonomy = "Type Mismatch"
        elif e.validator == "enum":
            error_taxonomy = "Invalid Value"
        elif e.validator == "minimum" or e.validator == "maximum":
            error_taxonomy = "Value Out of Range"

        # Use list comprehension to format the path nicely
        path = " -> ".join([str(p) for p in e.path])

        await update.message.reply_text(
            f"❌ Validation failed.\n\nError Type: {error_taxonomy}\n"
            f"Description: {e.message}\nPath: {path}"
        )
    except Exception as e:
        await update.message.reply_text(
            f"❌ An error occurred during validation: {str(e)}"
        )
            

from jsonschema import validate, ValidationError

def validate_json_payload(data: dict, schema: dict) -> dict:
    
    Validates a JSON payload against a schema and returns a structured result.
    
    try:
        validate(instance=data, schema=schema)
        return {
            "success": True,
            "taxonomy": None,
            "message": "Validation successful! The JSON data conforms to the schema.",
            "path": None
        }
    except ValidationError as e:
        error_taxonomy = "Validation Error"
        if e.validator == "required":
            error_taxonomy = "Missing Required Parameter"
        elif e.validator == "type":
            error_taxonomy = "Type Mismatch"
        elif e.validator == "enum":
            error_taxonomy = "Invalid Value"
        elif e.validator in ["minimum", "maximum"]:
            error_taxonomy = "Value Out of Range"

        path = " -> ".join([str(p) for p in e.path]) if e.path else None

        return {
            "success": False,
            "taxonomy": error_taxonomy,
            "message": e.message,
            "path": path
        }
    except Exception as e:
        return {
            "success": False,
            "taxonomy": "Internal Error",
            "message": str(e),
            "path": None
        }



from validators.json_validator import validate_json_payload

async def handle_validation(update: Update, context: ContextTypes.DEFAULT_TYPE, schema: dict, data: dict):
    result = validate_json_payload(data, schema)

    if result["success"]:
        await update.message.reply_text(f"✅ {result['message']}")
    else:
        await update.message.reply_text(
            f"❌ Validation failed.\n\n"
            f"Error Type: {result['taxonomy']}\n"
            f"Description: {result['message']}\n"
            f"Path: {result['path'] or 'N/A'}"
        )


"""

import enum

class ErrorType(enum.Enum):
    """
    Defines a clear and consistent taxonomy for validation errors.
    """
    MISSING_REQUIRED_PARAM = "Missing Required Parameter"
    ENUM_OR_TYPE_ISSUE = "Type or Enum Mismatch"
    VALUE_OUT_OF_RANGE = "Value Out of Range"
    HALLUCINATION = "Hallucination"
    OTHER_ISSUE = "Other Validation Issue"
    SUCCESS = "Validation Successful"
