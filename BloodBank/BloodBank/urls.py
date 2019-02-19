
from django.contrib import admin
from django.urls import path
from AppComponent import views

urlpatterns = [
    path('', views.loginUser),
    path('admin/', admin.site.urls),
    path('hello/', views.hello),
    path('login-user/', views.loginUser),
    path('SignUp_User/', views.SignUpUser),
    path('UserHome/', views.UserHome),
    path('GetUserDetail/', views.GetUserDetail),
    path('Site-Master/', views.SiteMaster),
    path('add-user/', views.AddUser),
    path('deac-user/', views.DeacUser),
    path('delete-user/', views.DeleteUser),
    path('user-history/', views.UserHistory),
    path('donor-list/', views.DonorList),
    path('Donor-Creation/', views.DonorResg),
    path('Deac-Donor/', views.DeacDonor),
    path('donor-delete/', views.DeleteDonor),
    path('donor-edit/', views.DonorEdit),
    
    path('Stock-Detail/', views.StockMasterList),
    path('Smp-Reg/', views.StockMasterResg),
    path('Smp-Dec/', views.StockMasterDeac),
    path('Smp-Delete/', views.StockMasterDelete),
    path('Smp-Edit/', views.StockMasterEdit),
    path('Stock-list/', views.StockMasterTabList),


    path('Contact-Us/', views.ContactUsMaster),
    path('Comment-List/', views.CommentList),
    path('del-Cmt/', views.DeleteCmt),
    path('hide-Cmt/', views.HideCmt),


    #User Personal Data
    path('user-Profile-edit/', views.EditProfile),
    path('chng-password/', views.ChangePassword),
    path('password-reset/', views.ForgotPassword),

    #Mail OPeration
    path('Mail-Master/',views.MailHomeMaster),
    path('Mail-Sent/',views.MailSentMaster)
]