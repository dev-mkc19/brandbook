from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponse
from .forms import UploadFileForm
from .logic import HeaderCheck


def handle_uploaded_file(f):
    try:
        filename = f.temporary_file_path()
    except:
        filename = f
    return filename

def upload_file(request):
    if request.method == 'POST':
        wb_file = handle_uploaded_file(request.FILES['fileUpload'])
        result = HeaderCheck(wb_file)
        return render(request, 'uploader/result_page.html', {'data': result})
    else:
        form = UploadFileForm()
    return render(request, 'uploader/upload_page.html', {'form': form})
