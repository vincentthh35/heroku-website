from django.shortcuts import render
from .models import StockInfo
import django_tables2 as tables
from .fetch import fetch

# class for generating table
class StockListTable(tables.Table):
    class Meta:
        model = StockInfo
        attrs = {'id': 'stock_list_table', 'class': 'table table-bordered dataTable'}
        fields = ['ticker', 'stock_name', 'sector']

# Create your views here.
def query(request):
    df = fetch()
    return render(request, 'query.html', {'df': df})

def showStockList(request):
    # stock_list = []
    full_stock_list = StockInfo.objects.all()
    table = StockListTable(full_stock_list)
    return render(request, 'feature/show_stock_list.html', {'stock_list_table': table})
