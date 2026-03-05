from django.contrib.auth.decorators import user_passes_test

def role_required(role):
    def decorator(view_func):
        return user_passes_test(
            lambda u: u.is_authenticated and u.groups.filter(name__iexact=role).exists(),
            login_url='/login/'  # ← add this line
        )(view_func)
    return decorator