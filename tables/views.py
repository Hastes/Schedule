from django.shortcuts import render, render_to_response,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Schedule,Group
from .parser2 import ParserTable

from django.contrib import messages

# Create your views here.

def button_page(request):
    group = Group.objects.all()
    success = 0
    lose = 0
    if request.POST:
        for f in request.FILES.getlist('file'):
            # https://docs.djangoproject.com/es/1.10/ref/contrib/postgres/fields/#arrayfield
            try:
                get = GetDataFromParser(f)
                name = get.group_name()
                success+=1
            except ValueError:
                messages.error(request, 'Документ %s не был добавлен(неверный формат)' % f.name)
                lose+=1
                continue
            except IndexError:
                lose+=1
                messages.error(request, 'В документе %s не было обнаружено расписание' % f.name)
                continue
            data_tr = equalizer(get.data_tr())
            instance,created = Group.objects.get_or_create(name_group = name)
            Schedule.objects.create(schedule = data_tr, group_key=instance)
        messages.info(request,'Успешно загружено: %s, неудачно: %s'%(success,lose))
    return render(request,'upload_html.html',{'group':group})

def get_sched(request,pk):
    sched = Schedule.objects.filter(group_key=pk)
    group = get_object_or_404(Group,id = pk)
    return render_to_response('sched.html',{'sched':sched,'group':group})


def equalizer(data):
    largest_length = 0 # To define the largest length

    for l in data:
        if len(l) > largest_length:
            largest_length = len(l) # Will define the largest length in data.

    for i, l in enumerate(data):
        if len(l) < largest_length:
            remainder = largest_length - len(l) # Difference of length of particular list and largest length
            data[i].extend([None for i in range(remainder)]) # Add None through the largest length limit
    return data

# def upload_html(request):
#     return HttpResponseRedirect('/')
# def replace_schedule(f):
#     dirname = timezone.now().strftime('%Y.%m.%d.%H.%M.%S')
#     media = "media_cdn"
#     path_file = '/old_html/'
#     path_replace = '/replace_html/' + dirname + "/"
#
#     try:
#         os.makedirs(media+path_replace)
#     except FileExistsError:
#         pass
#
#     try:
#         os.makedirs(media+path_file)
#     except FileExistsError:
#         pass
#
#     file = open(media+path_file+f.name,'wb+')    #Временный файл
#     for chunk in f.chunks():
#         file.write(chunk)
#     file.close()
#     p = ParserTable(f)
#     mass = p.data_tr(media+path_file+f.name)
#     shutil.rmtree(media+path_file)                   #удаление директории с временным файлом
#
#     new_file = open(media+path_replace+f.name,'w')
#     new_file.write("<table>\n")
#     for td in mass:
#         new_file.write("<tr>")
#         for tr in td:
#             new_file.write("<td>"+tr+"</td>\n")
#         new_file.write("</tr>\n")
#     new_file.write("</table>\n")
#     new_file.close()
#     return path_replace + f.name

class GetDataFromParser:
    def __init__(self,f):
        file = f.read()
        decode_list = ['cp1251','utf-8']
        for decode in decode_list:
            try:
                file = file.decode(decode)
                break
            except UnicodeDecodeError:
                pass
        if type(file) is not str:
            raise ValueError
        else:
            file = file.encode('utf-8')
        self.file = file

    def group_name(self):
        return ParserTable(self.file).name_group()

    def data_tr(self):
        return ParserTable(self.file).data_tr()
