from django.shortcuts import render
from django.forms.models import model_to_dict
from .models import CustomUser    

def show_user_data(request):
    user_id = request.GET.get('user_id')
    opp_obj = CustomUser.objects.get(id = user_id)

    return render(request, 'users/partials/user_show.html', { 'object':opp_obj })
    
