from jsonschema import validate, ValidationError
from bot.error_taxonomy import ErrorType
from typing import Any, Dict, List

class LLMConversationValidator:
    def __init__(self, tool_schema: dict):
        self.tool_schema = tool_schema
        self.errors = []

    def validate_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:

        errors: List[Dict[str, Any]] = []

        try:
            validate(instance=data, schema=self.tool_schema)
            return {
                "valid": True,
                "errors": []
            }
        except ValidationError as e:
            error_type = self._map_error_validation(e)
            errors.append({
                "type": error_type.value,
                "path": " -> ".join([str(p) for p in e.path]) or "(root)",
                "description": e.message
            })

            return {
                "valid": False,
                "errors": errors
            }
    def _map_error_validation(self, e:ValidationError ) ->ErrorType:
        if e.validator == "required":
            return ErrorType.MISSING_REQUIRED_PARAM
        elif e.validator == "type":
            return ErrorType.ENUM_OR_TYPE_ISSUE
        elif e.validator == "enum":
            return ErrorType.ENUM_OR_TYPE_ISSUE
        elif e.validator in ["minimum", "maximum"]:
            return ErrorType.VALUE_OUT_OF_RANGE
        else:
            return ErrorType.OTHER_ISSUE
