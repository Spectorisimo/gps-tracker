from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from . import services

gpsdata_services = services.GPSDataServicesV1()


def get_gps_data(request):
    data = gpsdata_services.get_all_data()[::-1]
    page_num = request.GET.get('page', 1)
    paginator = Paginator(data, 20)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'table.html', context={
        "page_obj": page_obj,
    })


def get_single_gps_data(request, pk):
    data = gpsdata_services.get_single_data(pk)
    return render(request, 'position.html', context={
        'latitude': data.latitude,
        'longitude': data.longitude,
    })


def get_current_position(request):
    data = gpsdata_services.get_all_data().last()

    return render(request,'current_position.html',context={
        'latitude':str(data.latitude),
        'longitude':str(data.longitude),
    })