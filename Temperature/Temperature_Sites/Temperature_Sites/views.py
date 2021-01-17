import time
import json

from django.http import HttpResponse
from django.shortcuts import render

from .worker import DataWorker

# dw = DataWorker()


class Views(object):
    def __init__(self):
        self.dw = DataWorker()

    def res_empty(self, request):
        print(request)
        return HttpResponse('Context of Empty')

    def res_index_html(self, request):
        print(request)
        context = dict(
            current_date=time.ctime()
        )
        return render(request, 'index.html', context)

    def res_locations(self, request):
        print(request)
        return HttpResponse(self.dw.locations.to_html())

    def res_locations_json(self, request):
        print(request)
        return HttpResponse(self.dw.locations.to_json())

    def res_search_locations(self, request, py):
        print(request, py)
        return HttpResponse(self.dw.search_by_pinyin(py).to_html())

    def res_plot(self, request):
        print(request)
        return HttpResponse(self.dw.canvas)
