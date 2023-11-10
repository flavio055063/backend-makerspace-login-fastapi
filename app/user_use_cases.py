from datetime import datetime, timedelta
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError
from decouple import config
from app.db.models import CustomerModel, BudgetModel
from app.schemas import Customer, Budget


SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES')

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def user_register(self, user: Customer):
        user_model = CustomerModel(
            customer_name = user.customer_name,
            password_hash = crypt_context.hash(user.password_hash),
            cpf = user.cpf,
            rua  =  user.rua,
            bairro =  user.bairro,
            cidade =  user.cidade,
            estado =  user.estado,
            cep =  user.cep,
            email =  user.email,
            isAdmin = False
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exists'
            )

    def user_login(self, user: Customer):
        user_on_db = self.db_session.query(CustomerModel).filter_by(email=user.email).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
        
        if not crypt_context.verify(user.password_hash, user_on_db.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
        
        exp = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

        payload = {
            'sub': user.email,
            'exp': exp
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'exp': exp.isoformat()
        }

    def verify_token(self, access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )
        
        user_on_db = self.db_session.query(CustomerModel).filter_by(email=data['sub']).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )
        return user_on_db

    def budgetRegister(self, budget: Budget, access_token):
        # Verify if the user is an admin
        user = self.verify_token(access_token)
        print(user.isAdmin)
        if not user.isAdmin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Only admins can create budgets'
            )

        budgetModel = BudgetModel(
            customer_id=user.customer_id,
            price=budget.price,
            isApproved=budget.isApproved,
            paymentStatus=budget.paymentStatus
        )
        try:
            self.db_session.add(budgetModel)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Failed to create the budget'
            )