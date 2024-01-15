from typing import Literal

SAFE_ACTIONS: Literal['list', 'retrieve'] = [
    'list',
    'retrieve'
]
PRIVATE_ACTIONS: Literal['create', 'update', 'partial_update', 'destroy'] = [
    'create',
    'update',
    'partial_update',
    'destroy'
]
