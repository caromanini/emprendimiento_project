from pydantic import BaseModel, field_validator

class ContactCreate(BaseModel):
    full_name: str
    phone_number: str

    @field_validator('phone_number')
    @classmethod
    def validate_phone(cls, value: str):
        value = value.strip()

        if not value.isdigit() or len(value) != 8:
            raise ValueError("El número debe ser de 8 dígitos.")
        
        return f"+569{value}"


class ContactUpdate(ContactCreate):
    pass
