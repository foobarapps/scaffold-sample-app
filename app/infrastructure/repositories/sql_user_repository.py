from typing import override

from scaffold.persistence import GenericSqlRepository

from app.domain.user import User, UserId, UserRepository
from app.infrastructure.persistence_model import User as UserDTO


class SqlUserRepository(GenericSqlRepository[User, UserId, UserDTO], UserRepository):
    @override
    def _map_entity_to_dto(self, entity: User) -> UserDTO:
        return UserDTO(
            id=entity.id.value,
            email=entity.email,
        )

    @override
    def _map_dto_to_entity(self, dto: UserDTO) -> User:
        return User(
            id=UserId(dto.id),
            email=dto.email,
        )
