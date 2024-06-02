from datetime import datetime

from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from ninja_extra import NinjaExtraAPI, api_controller, route
from ninja_extra.exceptions import APIException
from ninja_extra import status
from ninja_jwt import schema
from ninja_jwt.controller import TokenObtainSlidingController
from ninja_jwt.tokens import SlidingToken

from characters.models import Species, Character
from characters.schema import SpeciesSchema, CharacterSchema, CharacterCreateSchema, CharactersListSchema, \
    UpdateCharacterSchema, UserCreateSchema, UserTokenSchema

from ninja_jwt.authentication import JWTAuth

api = NinjaExtraAPI(
    version="0.0.1",
    title="Pokemons API",
    description="Best Pokemon API in the world",
)


@api_controller("/characters", tags=["Characters"], auth=JWTAuth())
class CharacterController:
    @route.get("", response=CharactersListSchema)
    def get_characters(self, start: int = 0, limit: int = 50):
        all_characters = Character.objects.all()
        paginator = Paginator(all_characters, limit)
        page_number = (start // limit) + 1
        page = paginator.get_page(page_number)

        return {
            "total_count": paginator.count,
            "page_number": page_number,
            "characters": page.object_list,
        }

    @route.get("{id}", response=CharacterSchema)
    def get_character_by_id(self, id):
        try:
            return Character.objects.get(id=id)
        except Character.DoesNotExist:
            exception = APIException(detail={
                "message": f"Character with id {id} not found.",
                "status": status.HTTP_404_NOT_FOUND,
                "type": "CHARACTER_NOT_FOUND",
            })
            exception.status_code = status.HTTP_404_NOT_FOUND

            raise exception

    @route.post("", response=CharacterSchema)
    def create_character(self, character: CharacterCreateSchema):
        try:
            character_data = character.model_dump()
            species = Species.objects.get(id=character_data["species"])
            character_model = Character.objects.create(
                name=character_data["name"],
                strength=character_data["strength"],
                species=species,
            )

            return character_model
        except IntegrityError as e:
            exception = APIException(detail={
                "message": "Character already exists",
                "status": status.HTTP_400_BAD_REQUEST,
                "type": "CHARACTER_DUPLICATION",
            })
            exception.status_code = status.HTTP_400_BAD_REQUEST

            raise exception

    @route.patch("{id}", response=CharacterSchema)
    def update_character(self, id: int, character_data: UpdateCharacterSchema):
        character = Character.objects.get(id=id)

        character_data = character_data.model_dump()

        if character_data["name"]:
            character.name = character_data["name"]

        if character_data["strength"]:
            character.strength = character_data["strength"]

        character.save()

        return character

    @route.delete("{id}", response={status.HTTP_204_NO_CONTENT: None})
    def delete_character(self, id: int):
        try:
            character = Character.objects.get(id=id)
            character.delete()

            return status.HTTP_204_NO_CONTENT, None
        except Character.DoesNotExist:
            exception = APIException(detail={
                "message": f"Character with id {id} not found.",
                "status": status.HTTP_404_NOT_FOUND,
                "type": "CHARACTER_NOT_FOUND",
            })
            exception.status_code = status.HTTP_404_NOT_FOUND

            raise exception


@api_controller("/species", tags=["Species"])
class SpeciesController:
    @route.get("", response=list[SpeciesSchema])
    def get_species(self):
        return Species.objects.all()

    @route.get("{id}", response=SpeciesSchema)
    def get_species_by_id(self, id):
        return Species.objects.get(id=id)


@api_controller("/users", tags=["Users"], auth=JWTAuth())
class UserController:
    @route.post("", response={204: None}, auth=None)
    def create_user(self, user_schema: UserCreateSchema):
        try:
            user_schema.create()
            return 204, None
        except Exception as e:
            print(e)
            exception = APIException(detail={
                "message": "Something went wrong",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "type": "INTERNAL_SERVER_ERROR",
            })
            exception.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            raise exception


@api_controller("/auth", tags=["Auth"])
class AuthController(TokenObtainSlidingController):
    @route.post("/login", response=UserTokenSchema)
    def login(self, user_token: schema.TokenObtainSlidingInputSchema):
        user = user_token._user
        token = SlidingToken.for_user(user)

        return UserTokenSchema(
            token=str(token),
            user=user,
            token_exp_date=datetime.fromtimestamp(token["exp"]),
        )


api.register_controllers(
    SpeciesController,
    CharacterController,
    UserController,
    AuthController,
)
