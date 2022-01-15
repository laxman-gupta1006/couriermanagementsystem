from selectors import EpollSelector
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import MySQLdb
import uuid
from django.db import connection
# from libs.dbutil import query_to_dicts
# Create your views here.

def home(request):
    return render(request,'Home.html')
def login_temp(request):
    return render(request,'login.html')
def aboutus(request):
    return render(request,'Aboutus.html')
def signin(request):
    return render(request,'signin.html')


from django.contrib.auth import authenticate, login

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/adminpanel')
        
    else:
        return redirect('/')

#SQL Queries

# CREATE TABLE Customer(Customer_Id varchar(355),Cust_name varchar(20),Phone_no int(10),Address varchar(40),PRIMARY KEY (Customer_Id));
# CREATE TABLE Shipment_details(S_ID varchar(355) NOT NULL, Origin varchar(20) NOT NULL, Destination varchar(20) NOT NULL,Customer_Id varchar(355),foreign key (Customer_Id) references Customer(Customer_Id), PRIMARY KEY(S_ID))
# CREATE TABLE Branch(Branch_Id varchar(355),City varchar(20),Address varchar(40),Pincode int(5),PRIMARY KEY (Branch_Id));
# CREATE TABLE Shipment_history(S_ID varchar(355),Date_in DATETIME,Date_out DATETIME,Location varchar(20),Branch_Id varchar(355),foreign key (Branch_Id) references Branch(Branch_Id));
# CREATE TABLE Employee(Emp_id varchar(355),Name varchar(20),Phone int(10),Branch_Id varchar(355),foreign key (Branch_Id) references Branch(Branch_Id),primary key (Emp_id));

@login_required(login_url='/login/')
def admin(request):
    return render(request,'admin/admin.html')

# @login_required(login_url='/login/')
def track_shipment(request):
    if request.method=="POST":
        s_id=request.POST.get('sid')
        query1=f"SELECT * FROM Shipment_history where S_ID='{s_id}'"
        try:
            c=connection.cursor()
            c.execute(query1)
            data=c.fetchall()
            print(data)
            result={'result':data,'status':'ok'}
        except:
            result={'status':'error'}
        if request.user.is_authenticated:
            return render(request,'admin/TrackShipment.html',result)
        else:
            print(result)
            return render(request,'trackshipment.html',result)
    if request.user.is_authenticated:
        return render(request,'admin/TrackShipment.html')
    else:
        return render(request,'trackshipment.html')
@login_required(login_url='/login/')
def add_shipment(request):
    result={'status':'wait'}
    if request.method=="POST":
        sender_name=request.POST.get('sender_name')
        sender_phone=request.POST.get('sender_phone')
        sender_address=request.POST.get('origin_city')
        pin_code=request.POST.get('origin_pincode')
        receivers_name=request.POST.get('receivers_name')
        receivers_phone=request.POST.get('receivers_phone')
        receivers_address=request.POST.get('dest_city')
        dest_pincode=request.POST.get('dest_pincode')
        branch=request.POST.get('branch')
        pick_up_date=request.POST.get('pick_up_date')
        s_id=uuid.uuid4()
        c_id=uuid.uuid4()
        s_id=str(s_id).replace("-","")
        c_id=str(c_id).replace("-","")
        try:
            query1=f"INSERT INTO Customer VALUES ('{c_id}','{sender_name}',{sender_phone},'{sender_address}')"
            query=f"INSERT INTO Shipment_details VALUES ('{s_id}','{sender_address}','{receivers_address}','{c_id}','{pin_code}','{dest_pincode}','{receivers_name}','{receivers_phone}','{branch}','{pick_up_date}')"
            c=connection.cursor()
            c.execute(query1)
            c.execute(query)
            result={'s_id':s_id,'c_id':c_id,'status':'ok'}
        except:
            result={'status':'error'}
        # print(x)
        # print(cust_name,cust_address,cust_phone,city,origin_city,dest_city,branch,pick_up_date)
    return render(request,'admin/AddShipment.html',result)

@login_required(login_url='/login/')
def update_shipment(request):
    if request.method=="POST":
        s_id=request.POST.get('sid')
        status=request.POST.get('status')
        date=request.POST.get('date')
        location=request.POST.get('location')
        branch_id=request.POST.get('branch')
        query1=f"INSERT INTO Shipment_history VALUES ('{s_id}','{status}','{date}','{location}','{branch_id}')"
        c=connection.cursor()
        try:
            c.execute(query1)
            result={'status':'updated'}
        except:
            result={'status':'error'}
        return render(request,'admin/UpdateShipment.html',result)
    return render(request,'admin/UpdateShipment.html')
    
    