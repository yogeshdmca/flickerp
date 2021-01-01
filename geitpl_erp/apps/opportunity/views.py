from django.shortcuts import render
from django.db.models import Q
from django.template.loader import render_to_string
from django.views.generic import View, ListView, DeleteView, CreateView, DetailView, UpdateView
from .forms import OpportunityCreateForm, LeadCreateForm, AttachmentCreateForm, OpportunitySchedulerForm, LeadSchedulerForm, ClientForm
from django.core.urlresolvers import reverse, reverse_lazy
from .models import Opportunity, Lead, OpportunityScheduler, LeadScheduler, Client
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
import json
from datetime import datetime, date, timedelta

class AdministrationOpportunityListView(ListView):
    template_name = 'opportunity/opportunity_list.html'
    queryset = Opportunity.objects.exclude(status='5')
    paginate_by = 25

    @property
    def get_user(self):
        if self.request.GET.get('user'):
            return self.request.GET.get('user')
        return self.request.user.id

    def get_queryset(self):
        if not self.request.GET:
            return self.queryset.filter(user_id=self.get_user, scheduler__result='1').distinct().order_by('scheduler__call_schedule')
        else:
            queryset =  self.queryset.filter(user_id=self.get_user)
            if self.request.GET.get('start_date') and self.request.GET.get('end_date'):
                start_date = self.request.GET.get('start_date')
                end_date = self.request.GET.get('end_date')
                queryset = queryset.filter(created_at__date__range = (start_date, end_date))
            if self.request.GET.get('call_result'):
                call_result = self.request.GET.get('call_result')
                queryset = queryset.filter(scheduler__result=call_result)
            if self.request.GET.get('country'):
                queryset = queryset.filter(country_id=self.request.GET.get('country'))
            if self.request.GET.get('q',False):
                q = self.request.GET.get('q')
                queryset = self.queryset.filter(
                    Q(firstname__icontains=q)|
                    Q(email__icontains=q)|
                    Q(skype__icontains=q)|
                    Q(contact__icontains=q)|
                    Q(description__icontains=q)
                    )

            #check order by 
            if self.request.GET.get('call_result'):
                queryset = queryset.distinct().order_by('scheduler__call_schedule')
            else:
                queryset = queryset.distinct().order_by('created_at')
            return queryset

    def get_context_data(self, **kwargs):
        context = super(AdministrationOpportunityListView, self).get_context_data(**kwargs)
        return context

class AdministrationOpportunityCreateView(CreateView):
    form_class = OpportunityCreateForm
    template_name = 'opportunity/partials/opportunity_create_form.html'
    success_url = reverse_lazy('opportunity:opportunities')

    def get_context_data(self, **kwargs):
        context = super(AdministrationOpportunityCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['opportunity_scheduler_form'] = OpportunitySchedulerForm(self.request.POST)
        else:
            context['opportunity_scheduler_form'] = OpportunitySchedulerForm()

        return context

    def form_valid(self, form):
        scheduler_form  = self.get_context_data()['opportunity_scheduler_form']
        form.instance.user = self.request.user
        if scheduler_form.is_valid():
            response = super(AdministrationOpportunityCreateView, self).form_valid(form)
            scheduler_obj = scheduler_form.save(commit=False)
            scheduler_obj.created_by = self.request.user
            scheduler_obj.result = '1'
            scheduler_obj.opportunity = form.instance
            scheduler_obj.save()
            #import pdb;pdb.set_trace()
        else:
            return self.form_invalid(form)

        if self.request.is_ajax():
            response.status_code = 212
        return response

    def form_invalid(self, form):
        response = super(AdministrationOpportunityCreateView, self).form_invalid(form)
        #import pdb;pdb.set_trace()
        if self.request.is_ajax():
            response.status_code = 222
        return response


class AdministrationOpportunityUpdateView(UpdateView):
    #form_class = OpportunityCreateForm
    template_name = 'opportunity/partials/opportunity_update_form.html'
    success_url = reverse_lazy('opportunity:opportunities')
    model = Opportunity
    exclude = ('user', 'created_at', 'modified_at')
    fields='__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(AdministrationOpportunityUpdateView, self).form_valid(form)
        if self.request.is_ajax():
            response.status_code = 212
        return response

    def form_invalid(self, form):
        response = super(AdministrationOpportunityUpdateView, self).form_invalid(form)
        if self.request.is_ajax():
            response.status_code = 222
        return response


class AdministrationOpportunityDetailView(DetailView):
    model = Opportunity
    template_name = 'opportunity/partials/opportunity_show.html'





# End of Opportunity View here and start Leave views 

class AdministrationLeadCreateView(CreateView):
    form_class = LeadCreateForm
    template_name = 'opportunity/lead_create.html'
    success_url = reverse_lazy('opportunity:leads')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user

        if self.request.POST['client'] == '':
            client_form = ClientForm(self.request.POST)
            client_form.instance.created_by = self.request.user
            client_form.instance.modified_by = self.request.user
            client_obj = client_form.save()
            form.instance.client = client_obj
        else:
            client_obj = Client.objects.get( id = self.request.POST['client'])
            form.instance.client = client_obj

        response = super(AdministrationLeadCreateView, self).form_valid(form)
        
        scheduler_form = LeadSchedulerForm(self.request.POST)
        if scheduler_form.is_valid():
            scheduler_form.instance.created_by = self.request.user
            scheduler_form.instance.modified_by = self.request.user
            scheduler_form.instance.result = '3'
            scheduler_obj = scheduler_form.save()
            scheduler_obj.lead = form.instance
            scheduler_obj.save()

        if 'document' in self.request.FILES:
            documents = self.request.FILES.getlist('document')
            for document in documents:
                attachment_form = AttachmentCreateForm(self.request.POST, {'document':document})
                if attachment_form.is_valid():
                    attachment_obj = attachment_form.save()
                    attachment_obj.content_object = form.instance
                    attachment_obj.save()
        if self.request.is_ajax():
            return JsonResponse({'success':1})
        return response

    def form_invalid(self, form):
        if self.request.is_ajax():
            attachment_form = AttachmentCreateForm()
            client_form = ClientForm()
            lead_scheduler_form = LeadSchedulerForm()
            html = render_to_string('opportunity/partials/lead_create_form.html', {'form':form, 'attachment_form':attachment_form, 'client_form':client_form, 'lead_scheduler_form':lead_scheduler_form}, request=self.request)
            return JsonResponse({'html':html, 'success':0})

        return super(AdministrationOpportunityCreateView, self).form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super(AdministrationLeadCreateView, self).get_context_data(**kwargs)

        if self.kwargs.get('opportunity_id',False):
            opp_dict = model_to_dict(Opportunity.objects.get(id=self.kwargs['opportunity_id']))
            [opp_dict.pop(key) for key in ['id', 'created_by', 'modified_by']]

            context['form'].initial = opp_dict
            context['opportunity_id'] = self.kwargs.get('opportunity_id')

        context['attachment_form'] = AttachmentCreateForm()
        context['client_form'] = ClientForm()

        return context





class AdministrationLeadListView(ListView):
    template_name = 'opportunity/lead_list.html'
    queryset = Lead.objects.all().order_by('-created_at')

    def get_queryset(self):
        start_date = self.request.GET.get('start_date') and self.request.GET.get('start_date') or date.today()
        end_date = self.request.GET.get('end_date') and self.request.GET.get('end_date') or None
        
        if self.request.GET.get('user'):
            if end_date:
                return self.queryset.filter(created_at__range = (start_date, end_date), created_by=self.request.GET.get('user'))
            else:
                return self.queryset.filter(created_at__date = start_date, created_by=self.request.GET.get('user'))
        else:
            if end_date:
                return self.queryset.filter(created_at__range = (start_date, end_date), created_by__in = self.request.user.get_all_childs_under_me())
            else:        
                return self.queryset.filter(created_at__date = start_date, created_by__in = self.request.user.get_all_childs_under_me())


    def get_context_data(self, **kwargs):
        context = super(AdministrationLeadListView, self).get_context_data(**kwargs)
        context['form'] = LeadCreateForm()
        context['attachment_form'] = AttachmentCreateForm()
        context['client_form'] = ClientForm()
        context['lead_scheduler_form'] = LeadSchedulerForm()

        return context


class AdministrationLeadDetailView(DetailView):
    model = Lead
    template_name = 'opportunity/lead_show.html'

    def get_context_data(self, **kwargs):
        context = super(AdministrationLeadDetailView, self).get_context_data(**kwargs)
        context['attachments'] = self.object.attachments.get_queryset()

        return context