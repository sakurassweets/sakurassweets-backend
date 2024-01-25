import re

from django.core.cache import cache


def delete_keys_with_prefix(prefix: str, pk: str) -> None:
    """Deletes cache keys by prefix.

    Provides smart delition by prefixes and pks. For example:
    if we are deleting all cache related to `product` prefix,
    we won't delete keys with `product_type` prefix.

    Also our cache mechanism caches status code and delete it
    in same way.

    Args:
        prefix: String object of cache prefix.
        pk: String object of primary key of exact object that cached.
            For example: product_retrieve_5
    """
    pk = str(pk)
    all_keys = cache.keys('*')
    keys_to_delete = [key for key in all_keys if key.startswith(prefix)]
    deleted_keys = set()
    for key in keys_to_delete:
        method = _extract_method_after_prefix(prefix, key)
        cache_pk = pk if pk in key else ''
        if _is_valid_key(key, prefix, method, cache_pk) and key not in deleted_keys:
            cache.delete(key)
            deleted_keys.add(key)


def _is_valid_key(key: str, prefix: str, method: str, pk: str = None) -> bool:
    """Validates cache key without pk.

    Args:
        key: String object of full cache key.
        prefix: String object of prefix. For example:
            `user` or `product`
        method: String object of method. For example:
            `retrieve` or `list`.
        pk: String object of primary key. Can be `None` for keys
            that doesn't have `pk`.
    Returns:
        Boolean that says is key valid (matches pattern) or not.
    """
    delete_prefix = f'{prefix}_{method}'
    delete_prefix_admin = f'{prefix}_{method}_admin'

    if pk:
        delete_prefix = delete_prefix + f'_{pk}'
        delete_prefix_admin = delete_prefix_admin + f'_{pk}'

    KEY_TEMPLATES = [delete_prefix,
                     f'{delete_prefix}_status_code',
                     f'{delete_prefix_admin}',
                     f'{delete_prefix_admin}_status_code',]
    return key in KEY_TEMPLATES


def _extract_method_after_prefix(prefix: str, full_key: str) -> str | None:
    """Extracts method from full key.

    For example: from `product_type_retrieve_1` will be extracted
    word `retrieve`.

    Args:
        prefix: string object of cache prefix.
        full_key: string object of full cache key. For example:
            `product_type_retrieve_6_status_code`.

    Returns:
        String object of method from full key. For example:
        from `product_type_retrieve_6_status_code` returns `retrieve`.

        If something gone wrong and pattern didn't match for some reason
        then will be returned `None`.
    """
    pattern = re.compile(f"{re.escape(prefix)}_([a-zA-Z0-9_]+)")
    match = pattern.match(full_key)
    if match:
        return match.group(1).split('_')[0]
    return None
