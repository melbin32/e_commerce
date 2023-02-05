from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name="create"),
    path("listing/<int:product_id>",views.product_page,name="product_page"),
    path("<int:product_id>/comment",views.add_comment,name="add_comment"),
    path("<int:product_id>/bid",views.make_bid,name="make_bid"),
    path("<int:product_id>/close_bid",views.close_bid,name="close_bid"),
    path("<int:product_id>/add_watchlist",views.add_watchlist,name="add_watchlist"),
    path("watchlist/",views.watchlist,name="watchlist")
]
