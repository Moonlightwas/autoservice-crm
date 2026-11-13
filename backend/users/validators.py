import re
from rest_framework import serializers


def validate_phone_number(value):
    if not value:
        return value

    cleaned = re.sub(r'[\s\+\-\(\)\.]', '', value)
    digits = cleaned[1:] if cleaned.startswith('+') else cleaned

    if not (10 <= len(cleaned) <= 20):
        raise serializers.ValidationError(
            "Phone number length must be 10 to 20"
            )

    if not (10 <= len(digits) <= 15):
        raise serializers.ValidationError(
            f"Phone number must contain 10-15 digits (got {len(digits)})"
        )

    if not re.match(r'^\d{10,15}$', cleaned):
        raise serializers.ValidationError("Invalid phone number format")

    return cleaned
