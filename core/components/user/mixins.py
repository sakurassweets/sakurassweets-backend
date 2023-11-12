from rest_framework import mixins


class UpdateRetrieveDestroyListUserMixin(mixins.UpdateModelMixin,
                                         mixins.RetrieveModelMixin,
                                         mixins.DestroyModelMixin,
                                         mixins.ListModelMixin):
    """
    Mixin provides default `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass
