import mimetypes

from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
def upload_to_path(instance, filename):
    now = timezone.now()
    return f"uploads/{now:%Y}/{now:%m}/{filename}"


class UploadedFile(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_files',
    )
    file = models.FileField(upload_to=upload_to_path)
    original_file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.original_file_name

    @property
    def is_image(self):
        content_type, _ = mimetypes.guess_type(self.original_file_name or self.file.name)
        return content_type is not None and content_type.startswith('image/')