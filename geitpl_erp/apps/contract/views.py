from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, View
from .forms import ContractCreateForm
from django.core.urlresolvers import reverse, reverse_lazy
from .models import *
from django.http import HttpResponse
from django.conf import settings
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

class AdministrationContractCreateView(CreateView):
    form_class = ContractCreateForm
    template_name = 'contract/contract_create.html'
    success_url = reverse_lazy('contract:create-contract')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        form.instance.is_active = True
        response = super(AdministrationContractCreateView, self).form_valid(form)
        return response   

    def get_context_data(self, **kwargs):
        context = super(AdministrationContractCreateView, self).get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
        return context


class AdministrationContractListView(ListView):
    template_name = 'contract/contract_list.html'
    queryset = Contract.objects.filter(is_active=True,user__is_active=True)
    paginate_by = 30
    def get_queryset(self):
        expiry_date = self.request.GET.get('expiry_date')
        if self.request.GET.get('user'):
            return self.queryset.filter(user = self.request.GET.get('user'))
        return self.queryset

class CommonContractListView(ListView):
    template_name = 'contract/contract_list.html'
    paginate_by = 20

    def get_queryset(self):
        return Contract.objects.filter(user=self.request.user)


class GenerateSalarySlip(View):
    def get(self, request, *args, **kwargs):
        try:
            pay_slip = request.user.pay_slips.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404
        
        rendered_html = render_to_string('users/salary_slip.html',{'user':request.user, 'pay_slip':pay_slip})

        pdf_file = HTML(string=rendered_html).write_pdf()

        http_response = HttpResponse(pdf_file, content_type='application/pdf')
        http_response['Content-Disposition'] = 'filename="PaySlip.pdf"'
        return http_response