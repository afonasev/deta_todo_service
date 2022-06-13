from fastapi_crudrouter import MemoryCRUDRouter

from app.ports.api.users.schemas import UserCreate, UserRead

router = MemoryCRUDRouter(
    schema=UserRead,
    create_schema=UserCreate,
    tags=['users'],
    prefix='/api/users',
)
