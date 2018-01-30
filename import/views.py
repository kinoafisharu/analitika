from django.shortcuts import render
from .resource import *
from django.contrib import messages
# Create your views here.
from .import_export_views import *
from .models import *
from django.utils.datastructures import MultiValueDictKeyError

def home(request):
    offers = Offers.objects.all()
    field = [f.name for f in Offers._meta.get_fields()]
    if request.POST:
        try:
            file = request.FILES['file']
            format_file = request.POST["file_format"]
            if file.name.split(".")[-1].lower() != format_file:
                messages.error(request, "Формат файла не подходит!")
            else:
                uploading_file = UploadingProducts({'file': file, 'format_file': format_file})
                if uploading_file:
                    messages.success(request, "Загружено")
                else:
                    messages.error(request, "Ошибка")
        except MultiValueDictKeyError:
            messages.error(request, "Выберите файл!")
    return render(request, 'home.html', locals())