from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('', views.home, name="home"),
    path(_('catalog') + '/<slug:slug>', views.catalog, name="catalog"),
    path(_('catalog'), views.catalog, name="catalog"),
    path(_('product') + '/<slug:slug>', views.product, name="product"),
    path(_('cart'), views.cart, name="cart"),
    path(_('cart/data'), views.data, name="data"),
    path(_('cart/checkout'), views.checkout, name="checkout"),
    path(_('cart/confirmation'), views.confirmation, name="confirmation"),
    path(_('about'), views.about, name="about"),
    path(_('contact'), views.contact, name="contact"),
    path('status/<str:number>', views.status, name="status"),
    path('available-products', views.availableProducts),
    path('search-product', views.searchProduct, name="search-product"),
    path('add-to-cart', views.addToCart, name="add-to-cart"),
    path('update-cart', views.updateCart, name="update-cart"),
    path('delete-from-cart', views.deleteFromCart, name="delete-from-cart"),
    path('update-data-cart', views.updateDataCart, name="update-data-cart"),
    path('place-order', views.placeOrder, name="place-order"),
    path('cancel-order', views.cancelOrder, name="cancel-order"),
    path('add-to-newsletter', views.addToNewsletter, name="add-to-newsletter"),
    path('cancel-newsletter/<str:email>',
         views.cancelNewsletter, name="cancel-newsletter"),
    path('send-message', views.sendMessage, name="send-message"),
]
