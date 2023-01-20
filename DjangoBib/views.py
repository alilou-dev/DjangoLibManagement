from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import render, redirect

# Not useful fot now
def password_reset_confirm(request, token):
  if request.method == "POST":
      password_reset_confirm_form = SetPasswordForm(request.POST)
      if password_reset_confirm_form.is_valid():
          password_reset_confirm_form.save()
          return redirect('reset/done/')

  password_reset_confirm_form = SetPasswordForm()
  return render(request=request, template_name="password/password_reset_confirm.html", context={"password_reset_confirm_form":password_reset_confirm_form})


