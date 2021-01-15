
from django.http import HttpResponse

from .worker import DataWorker

# dw = DataWorker()


class Views(object):
    def __init__(self):
        self.dw = DataWorker()

    def res_empty(self, request):
        print(request)
        return HttpResponse('Context of Empty')

    def res_locations(self, request):
        print(request)
        return HttpResponse(self.dw.locations.to_html())

    def res_search_locations(self, request, py):
        print(request, py)
        return HttpResponse(self.dw.search_by_pinyin(py).to_html())
