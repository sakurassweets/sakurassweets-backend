from django.core.cache import cache

from components.general.constants import CACHE_KEY_REGEX


def delete_keys_with_prefix(prefix: str, pk: str) -> None:
    """Deletes cache keys by prefix.

    Provides smart delition using complex RegEx. For example:
    if we are deleting all cache related to `product` prefix,
    we won't delete keys with `product_type` prefix.

    Also our cache mechanism caches `status code` and `page`
    number and delete in same way.

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
        if (match := CACHE_KEY_REGEX.match(key)) and (key not in deleted_keys):
            match_dict = match.groupdict()
            if not match_dict["prefix"] == prefix:
                continue
            if match_dict["pk"] and (not match_dict["pk"] == pk):
                continue
            cache.delete(key)
            deleted_keys.add(key)
