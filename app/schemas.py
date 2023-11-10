import re
from pydantic import BaseModel, validator


class Customer(BaseModel):
    customer_name: str | None = None
    cpf: str | None = None
    rua: str | None = None
    bairro: str | None = None
    cidade:  str | None = None
    estado: str | None = None
    cep: str | None = None
    email: str
    password_hash: str 

    @validator('customer_name')
    def validate_username(cls, value):
        pattern = r"^[A-Za-zÀ-ú\s]*$"
        if not re.match(pattern, value):
            raise ValueError('Name format invalid - use only valid characteres without numbers')
        return value
    
class Budget(BaseModel):
    price: float
    isApproved: bool
    paymentStatus: str


