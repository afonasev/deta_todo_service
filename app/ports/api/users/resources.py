from http import HTTPStatus
from typing import Optional

from aiohttp.client_exceptions import ClientResponseError
from deta import Deta

# async support version is alpha
from deta._async.client import AsyncBase, _AsyncBase  # noqa:WPS private imports
from fastapi import APIRouter, Depends, HTTPException, Query

from app.ports.api.users.schemas import UserCreate, UserRead
from app.settings import get_settings

ALREADY_EXISTS_ERROR_MESSAGE = 'already exists'

router = APIRouter(tags=['users'])


async def get_users_collection() -> AsyncBase:
    deta = Deta(get_settings().DETA_PROJECT_KEY)
    return deta.AsyncBase(get_settings().USERS_COLLECTION_NAME)


@router.get('/', response_model=list[UserRead])
async def get_users(
    users_collection: _AsyncBase = Depends(get_users_collection),
    limit: int = Query(10, le=100),
    last: Optional[str] = None,
) -> list[UserRead]:
    response = await users_collection.fetch(limit=limit, last=last)
    return [UserRead.parse_raw(user['value']) for user in response.items]


@router.get('/{user_id}', response_model=UserRead)
async def get_user(
    user_id: str,
    users_collection: _AsyncBase = Depends(get_users_collection),
) -> list[UserRead]:
    response = await users_collection.get(user_id)
    if not response:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, f'User with email {user_id} is not found'
        )
    return UserRead.parse_raw(response['value'])


@router.post('/', response_model=UserRead, status_code=HTTPStatus.CREATED)
async def create_user(
    new_user: UserCreate, users_collection: _AsyncBase = Depends(get_users_collection)
) -> UserRead:
    # we cannot use builtin key because deta dont have unique indexes
    try:
        response = await users_collection.insert(new_user.json(), key=new_user.email)
    except ClientResponseError as exc:
        if exc.code == HTTPStatus.CONFLICT:
            raise HTTPException(
                HTTPStatus.CONFLICT, f"User with email {new_user.email} already exists"
            ) from exc

        raise

    return UserRead.parse_raw(response['value'])


@router.delete('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_user(
    user_id: str,
    users_collection: _AsyncBase = Depends(get_users_collection),
) -> None:
    await users_collection.delete(user_id)
