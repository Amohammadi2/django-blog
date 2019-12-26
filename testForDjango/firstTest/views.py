from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import reporter, article, profile
from django.template import loader
from .forms import addArticleForm, deleteArticleForm, editArticleForm, userForm, profileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as log, logout as logo
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    allArticles = [x for x in article.objects.all()][:15]
    recentlyArticles = [x for x in article.objects.all()]
    recentlyArticles = recentlyArticles[::-1][0:5]
    popArticles = article.objects.all().order_by("-likes")[:5]
    template = loader.get_template("testForDjango/index.html")
    if request.user.username:
        form1 = addArticleForm(initial={'publisher':request.user})
        try:
            context = {
                "articles": allArticles,
                "recent": recentlyArticles,
                "form1": form1,
                "user": request.user,
                "image_url": request.user.profile.image.url.replace('firstTest',"").replace("//","/firsttest/"),
            }
        except:
            context = {
                "articles": allArticles,
                "recent": recentlyArticles,
                "form1": form1,
                "user": request.user,
            }
    else:
        context = {
            "articles": allArticles,
            "recent": recentlyArticles,
            "user": request.user,
        }
    context["popArticles"] = popArticles
    context["users"] = User.objects.all()   
    return HttpResponse(template.render(context, request))


def thanks(request):
    return HttpResponse('<h1>all inserted</h1><br><a href="/">return back</a>')


def showProfile(request, user_id):
    template = loader.get_template("testForDjango/showprofile.html")
    user = User.objects.get(pk=user_id)
    context = {
        'user': user,
        'profile_image': user.profile.image.url.replace("firstTest","").replace("//","/firstTest/")
    }
    return HttpResponse(template.render(context, request))

def want(request,article_id):
    wantedArticle = get_object_or_404(article,pk=article_id)
    template = loader.get_template("testForDjango/articleShow.html")
    return HttpResponse(template.render({"article": wantedArticle,"numberoflikes":len(wantedArticle.likerUsers.all()),'user':request.user}, request))

def addArticle(request):
    if request.method == "POST":
        gottenForm = addArticleForm(request.POST)
        if gottenForm.is_valid():
            gottenForm.save()
            return HttpResponseRedirect("/thanks")
        else:
            return HttpResponseRedirect("/")
    elif request.method == "GET":
        return HttpResponseRedirect("/")

def deleteArticle(request, article_ID):
    art = article.objects.get(pk=article_ID)
    art.delete()
    return HttpResponseRedirect("/deleted")


def deleted(request):
    return HttpResponse("<h1>the article deleted</h1><br><a href='/'>return back</a>")


def editArticle(request, article_ID):
    if request.method == "GET":
        art = get_object_or_404(article,pk=article_ID)
        template = loader.get_template("testForDjango/articleEdit.html")
        editForm = editArticleForm(initial={'articleContent':art.articleContent,'articleMain':art.articleMain,'publisher':request.user})
        context={
            "art_id": art.id,
            "form": editForm,
        }
        return HttpResponse(template.render(context, request))
    elif request.method == "POST":
        gottenForm = editArticleForm(request.POST)
        if gottenForm.is_valid():
            editedArticle = article.objects.filter(id=article_ID)
            editedArticle.update(
                articleMain= gottenForm.cleaned_data["articleMain"],
                articleContent= gottenForm.cleaned_data["articleContent"],
            )
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/")


def logout(request):
    logo(request)
    return HttpResponseRedirect("/")



def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username,password = password)
        if user:
            if user.is_active:
                log(request,user)
                return HttpResponseRedirect("/")
            else:
                return HttpResponse("your account is inactive")
        else:
            return HttpResponse("your information is not true")
    else:
        template = loader.get_template("testForDjango/login.html")
        context = {
            "form": userForm(),
        }
        return HttpResponse(template.render(context, request))
        


def signup(request):
    if request.method == "POST":
        user = User.objects.create_user(
            request.POST.get('username'),
            request.POST.get('email'),
        )
        user.set_password(request.POST.get('password'))
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        userprofile = profile(user = user)
        userprofile.save()
        user.save()
        return HttpResponse("you are signed up <a href='/'>return to site</a>")
    else:
        template = loader.get_template("testForDjango/signup.html")
        context = {
            "test": "this is test text !",
            "form": userForm(),
        }
        return HttpResponse(template.render(context, request))


def handleUploades(f):
    from datetime import datetime
    randomName = datetime.now().strftime("%H-%M-%S")    
    with open(f"firstTest/static/firstTest/img{randomName}.jpg", "wb+") as file:
        for chunk in f.chuncks():
            file.write(chunk)


def changeProfile(request):
    if request.method == "POST":
        form = profileForm(request.POST,request.FILES)
        if form.is_valid():
            user = request.user
            userprofile = user.profile
            userprofile.biography = form.cleaned_data['biography']
            userprofile.location = form.cleaned_data['location']
            userprofile.phonenumber = form.cleaned_data['phonenumber']
            if form.cleaned_data['image']:
                request.user.profile.image.delete()
                userprofile.image = form.cleaned_data['image']
            userprofile.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect("changeprofile/")
    else:
        userprofile = request.user.profile
        user = request.user
        template = loader.get_template("testForDjango/changeprofile.html")
        try:
            context = {
                "form": profileForm(initial={
                    'location':request.user.profile.location,
                    'biography':request.user.profile.biography,
                    'phonenumber':request.user.profile.phonenumber,
                    'image':request.user.profile.image,
                }),
                "user": user,
                "image_url": request.user.profile.image.url.replace('firstTest',"").replace("//","/firsttest/"),
            }
        except:
            context = {
                "form": profileForm(initial={
                    'location':request.user.profile.location,
                    'biography':request.user.profile.biography,
                    'phonenumber':request.user.profile.phonenumber,
                }),
                "user": user,
            }           
        return HttpResponse(template.render(context, request))


def like(request, article_id):
    if request.user.username: #check if a user has been logged in
        art = article.objects.get(pk=article_id)
        if request.user not in art.likerUsers.all():
            art.likerUsers.add(request.user)
            art.likes += 1
        art.save()
        data = {
            'number_of_likes': len(art.likerUsers.all())
        }
        return JsonResponse(data)
    else:
        return HttpResponse("you must login to your account to like or dislike this article")

def dislike(request, article_id):
    if request.user.username:
        art = article.objects.get(pk=article_id)
        if request.user in art.likerUsers.all():
            art.likerUsers.remove(request.user)
            art.likes -= 1
        art.save()
        data = {
            "number_of_likes": len(art.likerUsers.all()),
        }
        return JsonResponse(data)
    else:
        return HttpResponse("you must login to your account to like or dislike this article")


def search(request):
    searchQuery = request.GET.get("q")
    template = loader.get_template("testForDjango/search.html")
    articles = article.objects.filter(articleContent__icontains=searchQuery)
    context = {
        "searchQuery": searchQuery,
        "articles": articles,
    }
    return HttpResponse(template.render(context, request))


def allArticles(request):
    articles = article.objects.all()
    template = loader.get_template("testForDjango/allArticles.html")
    context = {
        "user": request.user,
        "articles": articles,
    }
    return HttpResponse(template.render(context, request))
