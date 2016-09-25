from django.shortcuts import render, render_to_response,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Schedule,Group,Faculty
from .parser2 import ParserTable
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages
from django.http import Http404

# Create your views here.
def schedule(request):
    return render(request,'faculty.html',{'faculty': Faculty.objects.all()})


def button_page(request,pk):
    group = Group.objects.filter(facult_key = pk)
    faculty = Faculty.objects.get(pk=pk)
    success = 0
    lose = 0
    if request.POST:
        if not request.user.is_authenticated:
            raise Http404
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
            instance,created = Group.objects.get_or_create(facult_key= Faculty.objects.get(pk=pk),name_group = name)
            Schedule.objects.create(schedule = data_tr, group_key=instance)
        messages.info(request,'Успешно загружено: %s, неудачно: %s'%(success,lose))
    return render(request,'upload_html.html',{'group':group,'faculty':faculty})

def get_sched(request,pk):
    try:
        sched = Schedule.objects.filter(group_key=pk)[0]
    except IndexError:
        sched = None
    return render(request,'sched.html',{'sched':sched})


def register(request):
    new_user = UserCreationForm(request.POST or None)
    if new_user.is_valid():
        new_user.save()
        return HttpResponse('Вы были успешно зарегистрированы')
    return render(request,'register&login.html',{'form':new_user})


def authview(request):
    args = {}
    args['form']  = AuthenticationForm()
    if request.POST:
        authuser = AuthenticationForm(data=request.POST)
        if authuser.is_valid():
            user = authenticate(username = request.POST["username"],password = request.POST["password"])
            messages.add_message(request,level = messages.INFO,message = "Вы успешно авторизованы")
            login(request,user)
            return HttpResponseRedirect('/')
    return render(request,'register&login.html',args)

def logoutview(request):
    logout(request)
    return HttpResponseRedirect('/')

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

class GetDataFromParser:
    def __init__(self, f):
        file = f.read()
        decode_list = ['cp1251', 'utf-8']
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
        self.parser = ParserTable(file)

    def group_name(self):
        return self.parser.name_group()

    def data_tr(self):
        return self.parser.data_tr()
