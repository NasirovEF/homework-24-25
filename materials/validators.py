from rest_framework import serializers


def validate_url(value):
    if not value.startswith("https://www.youtube.com/"):
        raise serializers.ValidationError("Разрешены ссылки только на Youtube")
    return value
