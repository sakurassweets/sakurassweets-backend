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
        prefix: string object of cache prefix.
        pk: string object of primary key of exact object that cached.
            For example: product_retrieve_5
    """
    all_keys = cache.keys('*')
    keys_to_delete = [key for key in all_keys if key.startswith(prefix)]
    deleted_keys = set()
    for key in keys_to_delete:
        method = _extract_method_after_prefix(prefix, key)
        # delete key for only specified pk
        if key in [f'{prefix}_{method}_{pk}', f'{prefix}_{method}_{pk}_status_code']:
            cache.delete(key)
            deleted_keys.add(key)
        # delete key if match prefix (for ex. product won't delete product_type keys)
        elif key == f'{prefix}_{method}' and key not in deleted_keys:
            cache.delete(key)
            deleted_keys.add(key)


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
