import csv
from django.http import HttpResponse

def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        if not fields:
            field_names = [field.name for field in opts.fields]
        else:
            field_names = fields
        #response = HttpResponse(mimetype='text/csv')
        #response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            writer.writerow(field_names)
            writer.writerow(['Transaction Type','Beneficiary  Code','Value Date','Debit A/C Number','Transaction Amount','Beneficiary Name','Beneficiary  A/c No.','IFSC Code','Bene Email ID','bene Mobile No','Customer Ref No.','Payment Narration']
)
        for obj in queryset:
            row = [getattr(obj, field)() if callable(getattr(obj, field)) else getattr(obj, field) for field in field_names]
            writer.writerow(row)
        return response
    export_as_csv.short_description = description
    return export_as_csv