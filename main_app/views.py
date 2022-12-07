from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
# Add LoginForm to this line...
from django.contrib.auth.forms import AuthenticationForm
# ...and add the following line...
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Cat model that's connected to the Database
from .models import Cat, Dog

# CRUD functions Cat:
class CatCreate(CreateView):
  model = Cat
  fields = '__all__'
  success_url = '/cats'

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.save()
    return HttpResponseRedirect('/cats')

class CatUpdate(UpdateView):
  model = Cat
  fields = ['name', 'breed', 'description', 'age']

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.save()
    return HttpResponseRedirect('/cats/' + str(self.object.pk))

@method_decorator(login_required, name='dispatch')
class CatDelete(DeleteView):
  model = Cat
  success_url = '/cats'

# CRUD functions Dog:
class DogCreate(CreateView):
  model = Dog
  fields = '__all__'
  success_url = '/dogs'

class DogUpdate(UpdateView):
  model = Dog
  fields = ['name', 'breed', 'description', 'age']

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.save()
    return HttpResponseRedirect('/dogs/' + str(self.object.pk))

class DogDelete(DeleteView):
  model = Dog
  success_url = '/dogs'

# Create your views here.
def index(request):
    cats = list(Cat.objects.all())
    return render(request, 'index.html', { 'cats': cats })

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def blog(request):
    return render(request, 'blog.html')

def cats_index(request):
    cats = list(Cat.objects.all())
    return render(request, 'cats/index.html', { 'cats': cats })

def cats_show(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(request, 'cats/show.html', { 'cat': cat })

def dogs_index(request):
    dogs = list(Dog.objects.all())
    return render(request, 'dogs/index.html', { 'dogs': dogs })

def dogs_show(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    return render(request, 'dogs/show.html', { 'dog': dog })

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'cats': cats})

def login_view(request):
     # if post, then authenticate (user submitted username and password)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/'+u)
                else:
                    print('The account has been disabled.')
            else:
                print('The username and/or password is incorrect.')
    else: # it was a get request so send the emtpy login form
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})