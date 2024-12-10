"""Here are the conversion from camelCase into snake_case and vice versa"""
import re

CAMEL_REGEX = re.compile('(?<=.)_(\\w)')
SNAKE_REGEX = re.compile('(?<=[a-z])([A-Z])')

def match_upper(match):
    return match.group(1).upper()

def match_snake(match):
    return f'_{match.group(1).lower()}'

def to_camelcase(text):
    """Transform the input into camelCase"""
    return CAMEL_REGEX.sub(match_upper, text)

def to_snake_case(text):
    """Transform the input into snake_case"""
    return SNAKE_REGEX.sub(match_snake, text)

def to_camelcase_data(data):
    """Transform the data to camelCase"""
    if isinstance(data, dict):
        return {to_camelcase(k): to_camelcase_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_camelcase_data(datum) for datum in data]
    else:
        return data

def to_snake_case_data(data):
    """Transform the data to snake_case"""
    if isinstance(data, dict):
        return {to_snake_case(k): to_snake_case_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_snake_case_data(datum) for datum in data]
    else:
        return data

class CamelCaseMixin:
    """Converts to camelCase"""
    def to_representation(self, *args, **kwargs):
        return to_camelcase_data(super().to_representation(*args, **kwargs))

    def to_internal_value(self, data):
        return super().to_internal_value(to_snake_case_data(data))