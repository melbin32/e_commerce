from django.contrib.auth.models import AbstractUser
from django.db import models



#Model to store the customer details
class User(AbstractUser):
    watchlist=models.ManyToManyField('Listing',related_name="watchlist",blank=True)
    def __str__(self):
        return f"{self.username}"


#Model to store product of each category
class Categories(models.Model):
    category=models.CharField(max_length=20,null=True)


#Model to store each listing posted by the user
class Listing(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="auctions")
    title=models.CharField(max_length=50)
    description=models.TextField(max_length=150)
    initial_bid=models.IntegerField()
    highest_bid=models.IntegerField(default=0)
    active=models.BooleanField(default=True)
    image=models.URLField(blank=True)
    highest_bidder=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.title} by {self.user}"


#Model to store the bids posted by user
class Bid(models.Model):
    amount=models.IntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="bidder")
    auction=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="Listing")

    def __str__(self):
        return f"{self.amount} on {self.auction} by {self.user}"


#Model to store the comments posted by each user
class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="commentor")
    text=models.TextField(max_length=300)
    auction=models.ForeignKey(Listing,on_delete=models.CASCADE)
    comment_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.text}"