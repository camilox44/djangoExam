from django.shortcuts import render, redirect
from datetime import datetime
from .models import User, Item
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    results = User.objects.register(request.POST)
    if isinstance(results, User):
        request.session['user_id'] = results.id
        messages.add_message(request, messages.SUCCESS, ''.format(results.username))
        return redirect('/home')
    else:
        for key in results:
            messages.add_message(request, messages.ERROR, results[key])
        return redirect("/")

def login(request):
    results = User.objects.login(request.POST)
    if isinstance(results, User):
        request.session['user_id'] = results.id
        messages.add_message(request, messages.SUCCESS, 'Welcome back, {}'.format(results.username))
        print(request.session['user_id'])
        return redirect('/home')
    else:
        for key in results:
            messages.add_message(request, messages.ERROR, results[key])
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def newitem(request):
    return render(request, 'newitem.html')

def additem(request):
    results = Item.objects.add_item(request.POST, request.session['user_id'])
    if isinstance(results, Item):
        messages.add_message(request, messages.SUCCESS, 'You successfully added a item')
        item = Item.objects.get(id=results.id)
        user = User.objects.get(id=request.session['user_id'])
        item.addwish.add(user)
        return redirect('/home')
    else:
        for key in results:
            messages.add_message(request, messages.ERROR, results[key])
    return redirect('/newitem')
    
def home(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You Are Not Logged In')
        return redirect('/')
    else:    
        addwish_items = User.objects.get(id=request.session['user_id']).addwish_items.all()
        items = Item.objects.all()
        user_log = User.objects.get(id=request.session['user_id'])
        for item in addwish_items:
            items = items.exclude(id=item.id)
        return render(request, 'home.html', {"items":items,"addwish_items":addwish_items, "user_log":user_log, "users":users})

def addtowish(request, item_id):
    item = Item.objects.get(id=item_id)
    user = User.objects.get(id=request.session['user_id'])
    item.addwish.add(user)
    return redirect('/home')

def removefromwish(request, item_id):
    item = Item.objects.get(id=item_id)
    user = User.objects.get(id=request.session['user_id'])
    item.addwish.remove(user)
    return redirect('/home')

def delete(request, item_id):
    Item.objects.filter(id=item_id).delete()
    return redirect('/home')

def iteminfo(request, item_id):
    item_info = Item.objects.get(id=item_id)
    user_wished = Item.objects.get(id=item_id).addwish.all()
    return render(request, 'item.html', {"item_info":item_info, "user_wished":user_wished})
    

# def pets(req):
#     fav_pets = Owner.objects.get(id=req.session["owner_id"]).fav_pets.all()
#     pets = Pet.objects.all()
#     for pet in fav_pets:
#         pets = pets.exclude(id=pet.id)
#     return render(req, "pets.html", {"pets": pets, "fav_pets": fav_pets})