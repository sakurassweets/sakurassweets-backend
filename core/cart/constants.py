from typing import Literal

SAFE_ACTIONS: Literal['list', 'retrieve'] = [
    'list',
    'retrieve'
]
PRIVATE_ACTIONS: Literal['update', 'partial_update', 'destroy'] = [
    'update',
    'partial_update',
    'destroy'
]
