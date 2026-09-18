from django.db import models
from django.utils import timezone
# Create your models here.
def upload_to_path(instance, filename):
    now = timezone.now()
    return f"uploads/{now:%Y}/{now:%m}/{filename}"


class UploadedFile(models.Model):
    file = models.FileField(upload_to=upload_to_path)
    original_file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.original_file_name