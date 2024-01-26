import re

# Simplified: prefix_method_admin?_pk?_page_{number}?_status_code?
# `?` means optional.
CACHE_KEY_REGEX = re.compile(
    r"^(?P<prefix>[a-zA-Z0-9_]+)(?:_(?P<method>list|retrieve))(?:_(?P<admin>admin))?"
    r"(?:_(?P<pk>\d+))?(?:_(?P<page>_\d+))?(?:_(?P<status_code>\w+))?$"
)
