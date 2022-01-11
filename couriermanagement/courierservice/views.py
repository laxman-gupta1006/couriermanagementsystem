from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request,'Home.html')
def login(request):
    return render(request,'login.html')
def aboutus(request):
    return render(request,'Aboutus.html')
def signin(request):
    return render(request,'signin.html')


##Admin Permission required to access these views

def admin(request):
    return render(request,'admin/admin.html')
def track_shipment(request):
    return render(request,'admin/TrackShipment.html')
def add_shipment(request):
    return render(request,'admin/AddShipment.html')
def update_shipment(request):
    return render(request,'admin/UpdateShipment.html')
    
    