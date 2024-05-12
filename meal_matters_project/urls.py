from django.contrib import admin
from django.urls import path
from donorApp.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",loginUser),
    path('logout', userLogout),
    path("singup",singup),
    path("home",home),
    path("add-food",addFood),
    path("food-list",foodList),
    path('delete-food/<int:pk>',deleteFood),
    path('edit-food/<int:pk>',editFood),
    path("donorcart",donorfoodcart),
    path('accept-request/<int:request_id>/', accept_request),
    path('reject-request/<int:request_id>/', reject_request),
    path("user-food-list",userFoodList),
    path("sendrequest/<int:pk>",send_request),
    path("myfoodcart",myfoodcart),
    path("viewfood/<int:pk>",view_food),
    path("sort-by-date",sortByDate)

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


