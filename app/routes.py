from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.depends import get_db_session, token_verifier
from app.user_use_cases import UserUseCases
from app.schemas import Customer, Budget

user_router = APIRouter(prefix='/user')
test_router = APIRouter(prefix='/test ', dependencies=[Depends(token_verifier)])


@user_router.post('/customer/register', status_code=201)
def user_register(user: Customer, db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    uc.user_register(user=user)
    return JSONResponse(
        content={'msg': 'success'},
        status_code=status.HTTP_201_CREATED
    )


@user_router.post('/customer/login')
def user_login(request_form_user: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    user = Customer(
        email = request_form_user.username,
        password_hash = request_form_user.password
    )
    print(user)

    auth_data = uc.user_login(user=user)
    return JSONResponse(
        content=auth_data,
        status_code=status.HTTP_200_OK
    )

@user_router.post('/customer/delete-user')
def user_login(access_token: str, db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    uc.user_deactivation(access_token=access_token)

    return JSONResponse(
        content={'msg': 'successfully deactivated'},
        status_code=status.HTTP_200_OK
    )


@user_router.post('/register-budget')
def budget_register(budget: Budget, access_token: str, db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    uc.budget_register(budget=budget, access_token=access_token)
    return JSONResponse(
        content={'msg': 'success'},
        status_code=status.HTTP_201_CREATED
    )

@test_router.get('/test')
def test_user_verify():
    return 'It works'
