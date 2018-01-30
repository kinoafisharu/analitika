import os
import sys
from .models import *
import xlrd
import django
from django.shortcuts import get_object_or_404, HttpResponse
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
os.environ['DJANGO_SETTINGS_MODULE'] = 'untitled1.settings'
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
django.setup()


class UploadingProducts(object):
    foreign_key_field = ["offer_tag"]
    key_field = ["slug"]
    model = Offers

    def __init__(self, data):
        data = data
        self.uploaded_file = data.get("file")
        self.parsing()

    def getting_related_model(self, field_name):
        related_model = self.model._meta.get_field(field_name).rel.to
        return related_model

    def getting_headers(self):
        s = self.s
        headers = dict()
        for column in range(s.ncols):
            value = s.cell(0,column).value
            headers[column] = value
        return headers

    def parsing(self):
        uploaded_file = self.uploaded_file
        wb = xlrd.open_workbook(file_contents=uploaded_file.read())
        s = wb.sheet_by_index(0)
        self.s = s
        headers = self.getting_headers()
        product_bulk_list = list()
        sub_bulk_list = []
        sub_key_bulk_list = []
        for row in range(1, s.nrows):
            row_dict = {}
            for column in range(s.ncols):
                value = s.cell(row, column).value
                field_name = headers[column]
                if field_name == 'id' and not value:
                    continue
                if field_name == "offer_sub_tag":
                    continue
                if field_name in self.foreign_key_field:
                    related_model = self.getting_related_model(field_name)
                    instance = get_object_or_404(related_model, tag_title=value)
                    value = instance
                row_dict[field_name] = value
            product_bulk_list.append(Offers(**row_dict))
            key = row_dict["slug"]
            sub_bulk_list.append(key)
        Offers.objects.bulk_create(product_bulk_list)
        for row in range(1, s.nrows):
            sub_dict = []
            for column in range(s.ncols):
                value = s.cell(row, column).value
                field_name = headers[column]
                if field_name in "offer_sub_tag":
                    a = [i for i in value.split(",")]
                    for i in range(0, len(a)):
                        instance = get_object_or_404(Subtags, tag_title=a[i])
                        value = instance
                        sub_dict.append(value)
                    sub_key_bulk_list.append(sub_dict)
        print(sub_key_bulk_list)
        ThroughModel = Offers.offer_sub_tag.through
        for i in range(len(sub_bulk_list)):
            for j in range(len(sub_bulk_list)):
                try:
                    try:
                        ThroughModel.objects.bulk_create([
                            ThroughModel(offers_id=get_object_or_404(Offers, slug=sub_bulk_list[i]).id,
                                         subtags_id=get_object_or_404(Subtags, tag_title=sub_key_bulk_list[i][j]).id),
                        ])
                    except MultipleObjectsReturned:
                        pass
                except IndexError:
                    continue
        return True