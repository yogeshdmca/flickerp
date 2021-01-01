from django.shortcuts import render
from django.forms.models import model_to_dict
from .models import Opportunity, Lead, OpportunityScheduler, LeadScheduler, Client
from .forms import OpportunityCreateForm, LeadCreateForm, AttachmentCreateForm, OpportunitySchedulerForm, LeadSchedulerForm, ClientForm, OpportunityCreateFormAPI
from django.http import HttpResponse, JsonResponse
from user.models import CustomUser
from django.views.decorators.csrf import csrf_exempt



def prospect_call_result_new(request,pk):
    form = OpportunitySchedulerForm()
    if request.is_ajax() and request.POST:
        form = OpportunitySchedulerForm(request.POST)
        if form.is_valid():
            prospect = form.save(commit=False)
            prospect.opportunity_id = pk
            prospect.created_by = request.user
            prospect.save()
            return JsonResponse({'success':1, 'action':'reload'})
        elif request.POST.get('result') in ['0','2','3','4']:
            prospect = OpportunityScheduler(result=request.POST.get('result'), description=request.POST.get('description',''),communication_type='7')
            prospect.opportunity_id = pk
            prospect.created_by = request.user
            prospect.save()
            return JsonResponse({'success':1, 'action':'reload'})

    return render(request, 'opportunity/partials/prospect_call_result_new.html', { 'form':form,'pk':pk})


def prospect_xedit(request):
    return 


def get_opportunity_data(request):
    opportunity_id = request.GET.get('opportunity_id')
    opp_obj = Opportunity.objects.get(id = opportunity_id)
    opp_dict = model_to_dict(opp_obj)
    [opp_dict.pop(key) for key in ['id', 'created_by', 'modified_by']]
    form = LeadCreateForm(initial = opp_dict)
    attachment_form = AttachmentCreateForm()
    client_dict = model_to_dict(opp_obj.client)
    [client_dict.pop(key) for key in ['id', 'created_by', 'modified_by']]
    client_form = ClientForm(initial=client_dict)
    lead_scheduler_form = LeadSchedulerForm()
    return render(request, 'opportunity/partials/lead_create_form.html', {'form':form, 'attachment_form':attachment_form, 'opportunity_id':opportunity_id, 'client_form':client_form, 'lead_scheduler_form':lead_scheduler_form })


def show_opportunity_data(request):
    opportunity_id = request.GET.get('opportunity_id')
    opp_obj = Opportunity.objects.get(id = opportunity_id)
    attachments = opp_obj.attachments.get_queryset()
    return render(request, 'opportunity/partials/opportunity_show.html', { 'object':opp_obj, 'attachments': attachments })
    

def show_lead_data(request):
    lead_id = request.GET.get('lead_id')
    lead_obj = Lead.objects.get(id = lead_id)
    attachments = lead_obj.attachments.get_queryset()
    return render(request, 'opportunity/partials/lead_show.html', { 'object':lead_obj, 'attachments': attachments })
    



def update_latest_schedule_lead(request):
    if request.is_ajax() and request.POST:
        lead_obj = Lead.objects.get(id = request.POST.get('lead_id'))
        lead_scheduler_obj = LeadScheduler.objects.get(id = request.POST.get('schedule_id'))
        lead_scheduler_obj.description = request.POST.get('description')
        lead_scheduler_obj.result = request.POST.get('scheduler_result')
        lead_scheduler_obj.save()

        if request.POST.get('scheduler_result') == '3':
            scheduler_form = LeadSchedulerForm(request.POST)
            if scheduler_form.is_valid():
                scheduler_form.instance.created_by = request.user
                scheduler_form.instance.modified_by = request.user
                scheduler_form.instance.result = '3'
                scheduler_obj = scheduler_form.save()
                scheduler_obj.lead = lead_obj
                scheduler_obj.save()

                return JsonResponse({'success':1, 'action':'reload'})

        elif request.POST.get('scheduler_result') == '2':
            return JsonResponse({'success':1, 'action':'create_estimation', 'lead_obj_id':lead_obj.id})

        return JsonResponse({'success':1, 'action':'reload'})





def get_client_data(request):
    client_id = request.GET.get('client')
    client_obj = Client.objects.get(id = client_id)
    return JsonResponse({'success':1, 'client_name':client_obj.client_name, 'email':client_obj.email, 'phone_number':client_obj.phone_number, 'skype':client_obj.skype})

@csrf_exempt
def create_opportunity_api(request):
    if request.method == 'POST':
        # description = request.POST.get('description')
        # looking_for_hire = request.POST.get('looking_for_hire')
        # technology = request.POST.get('technology')
        # skype = request.POST.get('skype')
        # email = request.POST.get('email')
        # contact = request.POST.get('contact')
        # admin = CustomUser.objects.filter(is_superuser=True).first()
        # Opportunity.objects.create(description=description, looking_for_hire=looking_for_hire, technology=technology, skype=skype, email=email, contact=contact, created_by=admin, modified_by=admin)
        form = OpportunityCreateFormAPI(data=request.POST)
        if form.is_valid():
            super_user = CustomUser.objects.filter(is_superuser=True,email='yogesh@geitpl.com').first()
            form.instance.user = super_user
            #form.instance.modified_by = super_user
            form.instance.status = '111'
            form.save()
            return JsonResponse({'status':'success','message':'Thanks, We will contact you soon...'})
        else:
            return JsonResponse({'status':'error','message':form.errors })
    
        # return JsonResponse({'success':1, 'msg':'Thanks, We will contact you soon...'})
        
        
        
        
