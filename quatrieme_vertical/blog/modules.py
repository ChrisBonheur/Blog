from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginator_articles(request, table_list):
    paginator = Paginator(table_list, 3)
    page = request.GET.get('page')
    try:
        table = paginator.page(1)
    except PageNotAnInteger:
        table = paginator.page(1)
    except EmptyPage:
        table = paginator.page(paginator.num_pages)
        
    return table
        
    