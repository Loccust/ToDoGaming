from src.models import db


def model_to_swagger_schema(model_class, exclude_fields=None, required_fields=None):
    exclude_fields = exclude_fields or []
    swagger_schema = {
        "type": "object",
        "properties": {},
        "required": []
    }

    for column in model_class.__table__.columns:
        if column.name in exclude_fields:
            continue

        swagger_type = "string"
        if isinstance(column.type, db.Integer):
            swagger_type = "integer"
        elif isinstance(column.type, db.Boolean):
            swagger_type = "boolean"

        swagger_schema["properties"][column.name] = {
            "type": swagger_type
        }

        if not column.nullable and not column.primary_key:
            swagger_schema["required"].append(column.name)

    if required_fields is not None:
        swagger_schema["required"] = required_fields

    return swagger_schema