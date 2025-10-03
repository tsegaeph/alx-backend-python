from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout

User = get_user_model()

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        logout(request) 
        user.delete()
        return redirect("/") 
