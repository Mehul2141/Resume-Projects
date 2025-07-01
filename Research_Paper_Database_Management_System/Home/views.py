from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib import messages

from Home.models import users_Model
from Home.models import research_Model
from Home.forms import researchforms

# Create your views here.

def index(request):
    return render(request, 'index.html')


def show_users(request):
    showall = users_Model.objects.all()
    return render(request, 'users_table.html', {"users_data": showall})


def show_research(request):
    showall = research_Model.objects.all()
    return render(request, 'research_table.html', {"research_data": showall})


def insert_research(request):
    if request.method=="POST":
        if request.POST.get('research_id') and request.POST.get('publisher_id') and request.POST.get('institute_id') and request.POST.get('type') and request.POST.get('name') and request.POST.get('publish_date') and request.POST.get('views') and request.POST.get('likes') and request.POST.get('dislikes'):
            saverecord = research_Model()
            saverecord.research_id = request.POST.get('research_id')
            saverecord.publisher_id = request.POST.get('publisher_id')
            saverecord.institute_id = request.POST.get('institute_id')
            saverecord.type = request.POST.get('type')
            saverecord.name = request.POST.get('name')
            saverecord.views = request.POST.get('views')
            saverecord.likes = request.POST.get('likes')
            saverecord.dislikes = request.POST.get('dislikes')
            saverecord.publish_date = request.POST.get('publish_date')
            saverecord.save()
            messages.success(request, 'Research Paper Inserted Successfully..!')
            return render(request, 'insert.html')
    else:
        return render(request, 'insert.html')
    
def Editresearch(request,id):
    editres=research_Model.objects.get(research_id=id)
    return render(request,'Edit.html',{"research_Model":editres})
    
def updateresearch(request,id):
    Updateresearch=research_Model.objects.get(research_id=id)
    form=researchforms(request.POST,instance=Updateresearch)
    if form.is_valid():
        form.save()
        messages.success(request,'Record update succesfully!')
        return render(request,'Edit.html',{"research_Model":Updateresearch})

def Delres(request,id):
    delres=research_Model.objects.get(research_id=id)
    delres.delete()
    showdata=research_Model.objects.all()
    return render(request,"research_table.html",{"research_data":showdata})

    