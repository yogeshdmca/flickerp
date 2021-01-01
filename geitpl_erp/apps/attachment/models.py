from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

import os

attachment_extension = {
    '.pdf': 'fa-file-pdf-o',
    '.xlsx': 'fa-file-excel-o',
    '.csv': 'fa-file-excel-o',
    '.txt': 'fa-file-text',
    '.jpg': 'fa-file-image-o',
    '.png': 'fa-file-image-o',
    '.tiff': 'fa-file-image-o',
    '.bmp': 'fa-file-image-o',
    '.zip': 'fa-file-archive-o',
    '.rar': 'fa-file-archive-o',
    '.tar': 'fa-file-archive-o',
    '.docx': 'fa-file-word-o',
    '.html': 'fa-file-code-o',
    '.py': 'fa-file-code-o',
    '.rb': 'fa-file-code-o',
    '.php': 'fa-file-code-o',
    '.java': 'fa-file-code-o',
    '.css': 'fa-file-code-o',
    '.js': 'fa-file-code-o',
    '.desktop': 'fa-file-code-o',
    '': 'fa-file',
    }

class Attachment(models.Model):
    document = models.FileField(upload_to='', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    content_type =   models.ForeignKey(ContentType, default=None, blank=True, null=True)
    object_id = models.PositiveIntegerField(default=None, blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    @property
    def class_for_attachment(self):
        name, extension = os.path.splitext(self.document.name)
        try:
            return attachment_extension[extension]
        except:
            return 'fa-file'
