import re
from pydantic import BaseModel, validator
from datetime import date

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

    @validator('email')
    def validate_email(cls, value):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise ValueError('Invalid email format')
        return value

    @validator('cpf')
    def validate_cpf(cls, value):
        pattern = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
        if not re.match(pattern, value):
            raise ValueError('Invalid CPF format. Expected format: 000.000.000-00')
        return value
    
    @validator('cep')
    def validate_cep(cls, value):
        pattern = r"^\d{5}-\d{3}$"
        if not re.match(pattern, value):
            raise ValueError('Invalid CEP format. Expected format: 00000-000')
        return value
    
    @validator('password_hash')
    def validate_password(cls, value):
        pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        if not re.match(pattern, value):
            raise ValueError('Invalid password format. Must contain 8 characters, with upper and lower case letters and at least 1 number and onde special character. ')
        return value
    
class Budget(BaseModel):
    serviceDescription: str
    category: str
    status: str



