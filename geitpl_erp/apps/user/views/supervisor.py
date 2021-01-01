from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from user.models import TlFeedback
from datetime import date, timedelta
from user.forms import TlFeedbackForm

from django.http import JsonResponse

class TlFeedbackView(View):
    template_name = "service/supervisor/emp_ratings.html"
    def get(self, request, *arg, **kwargs):
        if date.today() > date.today().replace(day=25):
            new_feedbacks=  request.user.tl_feedbacks.filter(created_at__month = date.today().month , created_at__year = date.today().year)
        elif date.today() < date.today().replace(day=8):
            new_feedbacks =  request.user.tl_feedbacks.filter(created_at__month = (date.today()-timedelta(days=30)).month , created_at__year = date.today().year)
        else:
            new_feedbacks = []
        return render(request, self.template_name, {"new_feedbacks": new_feedbacks})



class TlFeedbackNew(View):
    template_name = "service/supervisor/emp_ratings_form.html"


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
            return super(TlFeedbackNew, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *arg, **kwargs):
        instance = request.user.tl_feedbacks.get(pk=pk)
        form = TlFeedbackForm(instance = instance)
        return render(request, self.template_name, {'form':form,'instance':instance})

    def post(self,request,pk, *arg, **kwargs):
        if request.is_ajax():
            try:
                instance = request.user.tl_feedbacks.get(pk=pk)
                form = TlFeedbackForm(request.POST, instance = instance)
                rating = form.save()
                rating.rating_provided = True
                rating.save()
                data = {"msg":"Records updated",'status':'saved'}
            except:
                data = {"msg":"Invalid records",'status':'error'}
            return JsonResponse(data)
