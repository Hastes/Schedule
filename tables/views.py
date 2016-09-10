from django.shortcuts import render, render_to_response,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Schedule,Group
from .parser2 import ParserTable
from django.utils import timezone
import shutil
from string import whitespace
import os

# Create your views here.

def button_page(request):
    group = Group.objects.all()
    if request.POST:
        for f in request.FILES.getlist('file'):
            instance,created =  Group.objects.get_or_create(name_group = group_name(f))

            Schedule.objects.create(schedule_file=replace_schedule(f), group_key=instance)
    return render(request,'upload_html.html',{'group':group})

def get_sched(request,pk):
    sched = Schedule.objects.filter(group_key=pk)
    group = get_object_or_404(Group,id = pk)
    print(sched)
    return render_to_response('schedule.html',{'sched':sched,'group':group})


# def upload_html(request):
#     return HttpResponseRedirect('/')
def replace_schedule(f):
    dirname = timezone.now().strftime('%Y.%m.%d.%H.%M.%S')
    media = "media_cdn"
    path_file = '/old_html/'
    path_replace = '/replace_html/' + dirname + "/"

    try:
        os.makedirs(media+path_replace)
    except FileExistsError:
        pass

    try:
        os.makedirs(media+path_file)
    except FileExistsError:
        pass

    file = open(media+path_file+f.name,'wb+')    #Временный файл
    for chunk in f.chunks():
        file.write(chunk)
    file.close()
    mass = ParserTable.data_tr(media+path_file+f.name)
    shutil.rmtree(media+path_file)                   #удаление директории с временным файлом

    new_file = open(media+path_replace+f.name,'w')
    new_file.write("<table>\n")
    for td in mass:
        new_file.write("<tr>")
        for tr in td:
            new_file.write("<td>"+tr+"</td>\n")
        new_file.write("</tr>\n")
    new_file.write("</table>\n")
    new_file.close()

    return path_replace + f.name


def group_name(f):
    file = f.read()
    return ParserTable.name_group(file)