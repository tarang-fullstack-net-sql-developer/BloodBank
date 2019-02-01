"""CtrlPanel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AppComponent import views

urlpatterns = [path('', views.loginUser),
    path('admin/', admin.site.urls),
    path('hello/', views.hello),
    path('login-user/', views.loginUser),
    path('SignUp_User/', views.SignUpUser),
    path('UserHome/', views.UserHome),
    path('GetUserDetail/', views.GetUserDetail),
    path('Donor-Creation/', views.DonorResg),
    path('Deac-Donor/', views.DeacDonor),
    path('Site-Master/', views.SiteMaster),
    path('add-user/', views.AddUser),
    path('deac-user/', views.DeacUser),
    path('delete-user/', views.DeleteUser),
    path('user-history/', views.UserHistory),
    path('donor-list/', views.DonorList),

    path('Stock-Detail/', views.StockMasterList),
    path('Smp-Reg/', views.StockMasterResg),
    path('Smp-Dec/', views.StockMasterDeac),
    path('Smp-Delete/', views.StockMasterDelete),
    path('Smp-Edit/', views.StockMasterEdit),

    path('Contact-Us/', views.ContactUsMaster),
    path('Comment-List/', views.CommentList),
    path('del-Cmt/', views.DeleteCmt),
    path('hide-Cmt/', views.HideCmt),


    #User Personal Data
    path('user-Profile-edit/', views.EditProfile),
    path('chng-password/', views.ChangePassword),
    path('password-reset/', views.ForgotPassword)
]
