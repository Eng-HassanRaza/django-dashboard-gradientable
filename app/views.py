# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.template.loader import render_to_string
from django.http import HttpResponse,JsonResponse
from django import template
from .models import CarbonCodes
@login_required(login_url="/login/")
def index(request):
    carbon_obj = CarbonCodes.objects.all()
    context = {}
    context['segment'] = 'index'
    context['carbon_obj']=carbon_obj

    html_template = loader.get_template( 'tbl_bootstrap.html' )
    # html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))
@csrf_exempt
def get_tables_by_id(request):
    data = dict()
    if request.method == 'POST':
        search_by = request.POST['search_by']
        html_tmplt = loader.get_template('postgre_table.html')
        # search = request.POST.get('txtSearch')
        carbon_obj = CarbonCodes.objects.filter(phone_id=int(search_by))
        context = {
            'carbon_obj': carbon_obj
        }
        data['html_table'] = html_tmplt.render(
                                              context,
                                              request=request
                                              )
        return JsonResponse(data)


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
