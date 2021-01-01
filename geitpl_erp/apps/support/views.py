from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from support.models import Portfolio






class PortfolioListView(generic.ListView):
    model = Portfolio
    
class PortfolioCreateView(CreateView):
    model = Portfolio
    success_url = reverse_lazy('support:employee-portfolio-list')

    fields = ('title','description','skills','industry','cover','estimated_hours','taken_hours','client','live_url','developer')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(PortfolioCreateView, self).form_valid(form)
        if self.request.is_ajax():
            response.status_code = 212
        return response

    def form_invalid(self, form):
        response = super(PortfolioCreateView, self).form_invalid(form)
        if self.request.is_ajax():
            response.status_code = 222
        return response