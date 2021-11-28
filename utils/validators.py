from django.core.exceptions import ValidationError
from typing import Callable


def validate_char_ending(ending:str) -> Callable:

    def innerfunc(value:str) -> bool:
        if value.endswith(ending):
            return value
        else:
            raise ValidationError(f"Поле должно оканчиваться на '{ending}'")
    
    return innerfunc