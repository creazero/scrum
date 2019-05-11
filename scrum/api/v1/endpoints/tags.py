from fastapi import APIRouter

router = APIRouter()


@router.get('/tags')
def get_tags():
    return {'dumb': 'ok'}


@router.get('/tags/{tag_id}')
def get_tag(tag_id: int):
    return {'dumb': 'ok'}


@router.post('/tags')
def create_tag():
    return {'dumb': 'ok'}


@router.put('/tags/{tag_id}')
def update_tag(tag_id: int):
    return {'dumb': 'ok'}


@router.delete('/tags/{tag_id}')
def delete_tag(tag_id: int):
    return {'dumb': 'ok'}
