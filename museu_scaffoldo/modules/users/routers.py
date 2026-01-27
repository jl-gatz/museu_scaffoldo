from http import HTTPStatus

from fastapi import APIRouter, Depends

from museu_scaffoldo.modules.users.deps import get_current_user

from .schemas import MessageSchema, UserDB, UserPublic, UserSchema

router_user = APIRouter(prefix='/users', tags=['Users'])


# Teste com database falso
database = []


@router_user.get('/', status_code=HTTPStatus.OK, response_model=MessageSchema)
def read_users():
    return {'message': 'Olá, mundo!'}


@router_user.get('/me', status_code=HTTPStatus.OK, response_model=UserPublic)
def read_user_me(current_user: dict = Depends(get_current_user)):
    return current_user


@router_user.post(
    '/', status_code=HTTPStatus.CREATED, response_model=UserPublic
)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    return user_with_id
