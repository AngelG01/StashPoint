from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadedFileForm
from .models import UploadedFile

# Create your views here.
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.owner = request.user
            uploaded_file.save()
            return redirect('vault:gallery')
    else:
        form = UploadedFileForm()

    return render(request, 'vault/upload.html', {'form':form})

@login_required
def gallery(request):
    files = UploadedFile.objects.filter(owner=request.user).order_by('-uploaded_at')
    return render(request, 'vault/gallery.html', {'files':files})

@login_required
def delete_file(request, file_id):
    if request.method == 'POST':
        uploaded_file = UploadedFile.objects.filter(
            id=file_id,
            owner=request.user,
        ).first()
        if uploaded_file is not None:
            uploaded_file.file.delete(save=False)
            uploaded_file.delete()

    return redirect('vault:gallery')