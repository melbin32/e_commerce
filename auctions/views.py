from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from .forms import CreateBid,CommentForm
from .models import User,Listing,Comment,Bid
from django.core.exceptions import ValidationError


def index(request):
    return render(request,"auctions/index.html",{
            "listings": Listing.objects.all()
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

#View for Creating a listing
@login_required(login_url='login')
def create(request):
    if request.method=="POST":
        form=CreateBid(request.POST)
        if form.is_valid():
            new_auction=Listing(user=request.user,**form.cleaned_data)
            new_auction.highest_bid=new_auction.initial_bid
            new_auction.save()
            
        return render(request,"auctions/product_page.html",{
            "product":new_auction
        })

    else:
        form=CreateBid()
        
        return render(request,"auctions/create.html",{
            "create_form":form,"error":"Please login into your account to create a bid"
        })


#View for taking to a specific product page
def product_page(request,product_id):
    product=Listing.objects.get(pk=product_id)
    make_comment=CommentForm()
    comment=Comment.objects.filter(auction=product)
    return render(request,"auctions/product_page.html",{
        "product":product,
        "comment":comment,
        "make_comment":make_comment
    })

#making a comment
def add_comment(request,product_id):
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            product=Listing.objects.get(pk=product_id)
            new_comment=Comment(user=request.user,auction=product,**form.cleaned_data)
            new_comment.save()
        return product_page(request,product_id=product_id)


#making a bid
@login_required(login_url='login')
def make_bid(request,product_id):
    if request.method=="POST":
        amount=int(request.POST["amount"])
        product=get_object_or_404(Listing,id=product_id)
        if amount>product.highest_bid:
            product.highest_bid=amount
            make_bid=Bid(user=request.user,auction=product,amount=amount)
            product.highest_bidder=request.user
            product.save()
            make_bid.save()
        else:
            error="Bid must be greater than the curretn highest bid"
        return product_page(request,product_id=product_id)

# closing a bid
def close_bid(request,product_id):
    product=get_object_or_404(Listing,id=product_id)
    if(product.user==request.user):
        product.active=False
        product.save()
    return product_page(request,product_id=product_id)


# view for displaying the watchlist
@login_required(login_url='login')
def watchlist(request):
    watchlist=request.user.watchlist.all()
    return render(request,"auctions/watchlist.html",{
        "watchlist":watchlist
    })

def add_watchlist(request,product_id):
    product=get_object_or_404(Listing,id=product_id)
    request.user.watchlist.add(product)
    request.user.save()
    return product_page(request,product_id=product_id)