from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from museu_scaffoldo.modules.users.deps import get_current_user

from .schemas import Message, UserDB, UserList, UserPublic, UserSchema

router_user = APIRouter()


# Teste com database falso
database = []


@router_user.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}


@router_user.get(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user_by_id(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    user_with_id = database[user_id - 1]
    return user_with_id


@router_user.get('/me', status_code=HTTPStatus.OK, response_model=UserPublic)
def read_user_me(current_user: dict = Depends(get_current_user)):
    return current_user


@router_user.post(
    '/', status_code=HTTPStatus.CREATED, response_model=UserPublic
)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@router_user.put('/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id
    return user_with_id


@router_user.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    del database[user_id - 1]
    return {'message': 'Usuário deletado com sucesso!'}
