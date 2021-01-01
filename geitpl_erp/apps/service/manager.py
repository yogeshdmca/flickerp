from django.db import models
from django.db import transaction, IntegrityError

from service import SERVICE_STATUS


class ServiceManager(models.Manager):

    def services(self, *args, **kwargs):
        user = kwargs.pop('user', [])
        if user:
            #raise ValueError('one usermodel  kwargs needed to execute this method')
            return self.get_queryset().filter(assigned_to__in=user.get_all_supervisors_under_me(), *args, **kwargs)
        else:
            return self.get_queryset().filter(*args, **kwargs)


def add_methods(cls, value):
    def model_status(self, *args, **kwargs):
        return self.services(status=value[0], *args, **kwargs)
    model_status.__doc__ = value[1]
    model_status.__name__ = value[0]
    setattr(cls, model_status.__name__, model_status)

for status in SERVICE_STATUS:
    add_methods(ServiceManager, status)


class TimeSheetManager(models.Manager):

    def timeheet_this_month(self, *args, **kwargs):
        from attendance.models import this_month_start_end_date
        start_date, end_date, total_days = this_month_start_end_date()
        return self.get_queryset().filter(date__gte=start_date, date__lte=end_date, *args, **kwargs)

    def update_or_create(self, **kwargs):
        assert kwargs, \
            'update_or_create() must be passed at least one keyword argument'
        obj, created = self.get_or_create(**kwargs)
        defaults = kwargs.pop('defaults', {})
        if created:
            return obj, True, False
        else:
            try:
                params = dict([(k, v)
                               for k, v in kwargs.items() if '__' not in k])
                params.update(defaults)
                for attr, val in params.items():
                    if hasattr(obj, attr):
                        setattr(obj, attr, val)
                sid = transaction.savepoint()
                obj.save(force_update=True)
                transaction.savepoint_commit(sid)
                return obj, False, True
            except IntegrityError as e:
                transaction.savepoint_rollback(sid)
                try:
                    return self.get(**kwargs), False, False
                except self.model.DoesNotExist:
                    raise e
