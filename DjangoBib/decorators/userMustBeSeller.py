from django.contrib.auth.decorators import login_required, user_passes_test

user_sellerStatus_required = user_passes_test(lambda user: user.has_perm('Account.add_book'), login_url='/home')


def perm_seller_required(view_func):
    decorated_view_func = login_required(user_sellerStatus_required(view_func))
    return decorated_view_func