from django.contrib import admin

from vault.models import UploadedFile

# Register your models here.
@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('original_file_name', 'uploaded_at')
