from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from scrum.api.utils.db import get_db
from scrum.api.utils.security import get_current_user
from scrum.api.utils.shared import validate_project
from scrum.db_models.user import User
from scrum.models.tag import TagCreate, Tag
from scrum.repositories.tags import TagRepository

router = APIRouter()


@router.get('/tags')
def get_tags():
    return {'dumb': 'ok'}


@router.get('/tags/{tag_id}')
def get_tag(tag_id: int):
    return {'dumb': 'ok'}


@router.post('/tags', response_model=Tag)
def create_tag(
        tag_in: TagCreate,
        *,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    validate_project(current_user.id, tag_in.project_id, current_user.is_superuser,
                     session=session, check_owner=True)
    tag_repo = TagRepository(session)
    tag = tag_repo.create(tag_in)
    return tag


@router.put('/tags/{tag_id}')
def update_tag(tag_id: int):
    return {'dumb': 'ok'}


@router.delete('/tags/{tag_id}')
def delete_tag(tag_id: int):
    return {'dumb': 'ok'}
