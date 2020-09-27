from django.shortcuts import render
from django.views.generic.base import TemplateView

from stock.models import StockRecord

import django_tables2 as tables

def rankingEntries(request):
    context = {}
    context['title_dict'] = StockRecord.title_dict
    return render(request, 'ranking/ranking_entry_template.html', context)

'''
IMPORTANT: use class-based view
https://stackoverflow.com/questions/60030447/django-dynamic-url-pattern-based-on-model-names-how-to-do-it
'''

class RankingTable(tables.Table):
    class Meta:
        model = StockRecord
        # modify table attributes here
        attrs = {'id': 'table_name', 'class': 'table table-bordered table-striped'}
        # displayed fields
        fields = ['ranking_number', 'stock_info.ticker', 'stock_info.stock_name']

# Ranking view functions

class RankingView(TemplateView):
    template_name = 'ranking/ranking_template.html'
    # define usable variable
    # TODO:
    record_type = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ranking_list = StockRecord.objects.filter(record_type=self.record_type)
        if ranking_list.exists():
            context['last_modified'] = ranking_list[0].last_modified
        table = RankingTable(ranking_list)
        context['ranking_table'] = table
        context['ranking_title'] = StockRecord.title_dict[self.record_type]
        return context
