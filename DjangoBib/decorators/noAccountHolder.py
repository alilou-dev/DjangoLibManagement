from django.contrib.auth.decorators import login_required, user_passes_test

user_account_required = user_passes_test(lambda user: not user.has_perm('Account.change_account'), login_url='/home')

def no_userHasAccount_required(view_func):
  decorated_view_func = login_required(user_account_required(view_func))
  return decorated_view_func