from ninja_extra import status
from ninja_extra.exceptions import APIException
from ninja_schema import Schema, ModelSchema, model_validator
from django.contrib.auth import get_user_model

from characters.models import Character

UserModel = get_user_model()


class SpeciesSchema(Schema):
    id: int
    name: str


class CharacterCreateSchema(ModelSchema):
    class Config:
        model = Character
        include = ("name", "strength", "species")


class CharacterSchema(Schema):
    id: int
    name: str


class CharactersListSchema(Schema):
    total_count: int
    page_number: int
    characters: list[CharacterSchema]


class UpdateCharacterSchema(ModelSchema):
    class Config:
        model = Character
        include = ("name", "strength")


class UserCreateSchema(ModelSchema):
    class Config:
        model = UserModel
        include = ("first_name", "last_name", "username", "email", "password")

    @model_validator("username")
    def validate_unique_username(cls, value):
        if UserModel.objects.filter(username__iexact=value).exists():
            exception = APIException("Username already exists")
            exception.status_code = status.HTTP_400_BAD_REQUEST

            raise exception
        return value

    def create(self):
        return UserModel.objects.create_user(**self.dict())


from datetime import datetime
from typing import Optional


class UserSchema(ModelSchema):
    class Config:
        model = UserModel
        include = ("id", "username", "email")


class UserTokenSchema(Schema):
    token: str
    user: UserSchema
    token_exp_date: Optional[datetime]
