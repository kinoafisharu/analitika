from django.shortcuts import render
from .resource import *
from django.contrib import messages
# Create your views here.
from .import_export_views import *
from .models import *
from django.utils.datastructures import MultiValueDictKeyError

def home(request):
    offers = Offers.objects.all()
    if request.POST:
        try:
            file = request.FILES['file']
            uploading_file = UploadingProducts({'file': file})
            if uploading_file:
                messages.success(request, "Загружено")
            else:
                messages.error(request, "Ошибка")
        except MultiValueDictKeyError:
            messages.error(request, "Выберите файл!")
    return render(request, 'home.html', locals())