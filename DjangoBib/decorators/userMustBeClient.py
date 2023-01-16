from django.contrib.auth.decorators import login_required, user_passes_test

user_clientStatus_required = user_passes_test(lambda user: not user.has_perm('Account.add_book'), login_url='/home')


def perm_client_required(view_func):
    decorated_view_func = login_required(user_clientStatus_required(view_func))
    return decorated_view_func