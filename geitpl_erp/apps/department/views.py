# from django.shortcuts import render
# from django.views.generic import View, ListView, DeleteView, CreateView
# from .forms import DepartmentCreateForm
# from django.core.urlresolvers import reverse, reverse_lazy
# from .models import Department

# # Create your views here.# Create new User

# class AdministrationDepartmentCreateView(CreateView):
#     form_class = DepartmentCreateForm
#     template_name = 'department/department_create.html'
#     success_url = reverse_lazy('department:department-create')

#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         form.instance.modified_by = self.request.user
#         return super(AdministrationDepartmentCreateView, self).form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super(AdministrationDepartmentCreateView, self).get_context_data(**kwargs)
#         context['departments'] = Department.objects.all()
#         return context
