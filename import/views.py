from django.shortcuts import render
from .resource import *
from django.contrib import messages
# Create your views here.
from .import_export_views import *


def home(request):
    if request.POST:
        file = request.FILES['file']
        uploading_file = UploadingProducts({'file': file})
        if uploading_file:
            messages.success(request, "Загружено")
        else:
            messages.error(request, "Ошибка")
    return render(request, 'home.html', locals())