from django.shortcuts import render
from .models import StockInfo
import django_tables2 as tables
from .fetch import fetch

# class for generating table
class StockListTable(tables.Table):
    class Meta:
        model = StockInfo
        # modify table attributes here
        attrs = {'id': 'stock_list_table', 'class': 'table table-bordered table-striped'}
        fields = ['ticker', 'stock_name', 'sector']

# Create your views here.
def query(request):
    df = fetch()
    return render(request, 'query.html', {'df': df})

def showStockList(request):
    full_stock_list = StockInfo.objects.all()
    table = StockListTable(full_stock_list)
    return render(request, 'feature/show_stock_list.html', {'stock_list_table': table})

def filterStock(request):
    if request.method == 'POST':
        form = MyForm(request.POST, extra=request.POST.get('extra_field_count'))
        if form.is_valid():
            print('valid')
    else:
        form = MyForm()
    return render(request, 'feature/filter_stock.html', { 'form' : form})
