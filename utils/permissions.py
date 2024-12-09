from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

class RoleRequiredMixin(AccessMixin):
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        # check if login
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        user_role = request.session.get('user_role')
        if not (request.user.is_superuser or user_role in self.allowed_roles):
            return HttpResponseRedirect(reverse_lazy('user_login'))

        return super().dispatch(request, *arg, **kwargs)