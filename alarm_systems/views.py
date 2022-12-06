from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View

from alarm_systems.models import Customer


# Create your views here.


def home(request):
    return render(request, 'home/home.html')


class MainView(View):
    def get(self, request):
        customers_all = Customer.objects.all().order_by('last_name')
        return render(
            request,
            'home/alarm_systems_main_view.html',
            context={
                'customers_all': customers_all
            })
