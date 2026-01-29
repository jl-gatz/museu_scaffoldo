from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserList(BaseModel):
    users: list[UserPublic]


class UserDB(UserSchema):
    id: int

    def to_dict(self) -> dict[str, str]:
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
        }


class Message(BaseModel):
    message: str
