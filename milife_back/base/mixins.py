

class NestedQuerysetMixin(object):
    """
    Enables nested url in drf.
    eg /user/:pk/documents/:doc-pk
    etc.
    """
    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        if user_pk:
            return self.queryset.filter(user=str(user_pk))
        return self.queryset
