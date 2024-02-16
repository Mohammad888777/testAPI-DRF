from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def hande_paginator(obj,perPage,page):
    paginator=Paginator(obj,perPage)
    try:
        result=paginator.page(page)
    except PageNotAnInteger:
        result=paginator.page(1)
    except EmptyPage:
        result=paginator.page(paginator.num_pages)
    return result
