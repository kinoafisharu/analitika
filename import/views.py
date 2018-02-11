from django.shortcuts import render
from .resource import *
from django.contrib import messages
# Create your views here.
from .import_export_views import *
from .models import *
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from urllib.parse import urlsplit
import requests

def home(request):
    offers = Offers.objects.all().order_by("-created")
    field = [f.name for f in Offers._meta.get_fields()]
    if request.POST:
        if "upload" in request.POST:
            for i in offers:
                if i.offer_image_url and not i.offer_photo:
                    r = requests.get(i.offer_image_url, verify=False)
                    if r.status_code == requests.codes.ok:
                        img_temp = NamedTemporaryFile()
                        img_temp.write(r.content)
                        img_temp.flush()
                        img_filename = urlsplit(i.offer_image_url).path[1:]
                        i.offer_photo.save(img_filename, File(img_temp), save=True)
                    continue
            messages.success(request, "Фото загружено")
            return render(request, 'home.html', locals())
        else:
            try:
                file = request.FILES['file']
                format_file = request.POST.get("file_format", False)
                if file.name.split(".")[-1].lower() != format_file:
                    messages.error(request, "Формат файла не подходит!")
                else:
                    uploading_file = UploadingProducts({'file': file, 'format_file': format_file})
                    if uploading_file.parsing():
                        messages.success(request, "Загружено и обновлено")
                    else:
                        messages.error(request, "Ошибка")
            except MultiValueDictKeyError:
                messages.error(request, "Выберите файл!")
    return render(request, 'home.html', locals())