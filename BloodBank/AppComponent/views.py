from django.shortcuts import render, redirect
import datetime
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q

from django.core.mail import send_mail
from django.conf import settings

#Email Library
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
#End of Email Library

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from AppComponent.models import LoginUser
from AppComponent.models import RegisterUser
from AppComponent.models import DonorRegistration
from AppComponent.models import StockDetail
from AppComponent.models import LoginHistory
from AppComponent.models import ContactUs
from AppComponent.models import UsersImage
from AppComponent.models import MailMaster
from AppComponent.models import UserRoles
from django.db.models import *

import string
from random import *

import base64
  
def hello(request):
    return HttpResponse("<h2>Hello, Welcome to Django!</h2>")

def loginUser(request):  
    if request.method == "POST":
        userId = request.POST.get('userTxt')
        userPasswd = request.POST.get('userPass')
        RetData = LoginUser.objects.filter(Q(UserId = userId) & Q(Password = userPasswd))
        RetData_json = serializers.serialize('json', RetData)

        if RetData.count() > 0:
            for res in RetData:
                if res.isActive == 1:
                    request.session['_UserId'] = res.UserId
                    request.session['_PkId'] = res.pk
                    request.session['UserRoleId'] = res.UserRoleId
                    CreateLoginHistory(res.UserId)
                else:
                    LoginStatus = 'User is In-Active !!'
                    return render(request,"Login.html",{'LoginStatus' : LoginStatus})
            return redirect("/Site-Master/",{"UsrRoleId":request.session['UserRoleId']})
        else:
            LoginStatus = 'Invaid User ID and Password !!'
        return render(request,"Login.html",{'LoginStatus' : LoginStatus})

    if request.method == "GET":
        return render(request,"Login.html")

def IndexPage(request):
    return render(request,'SiteMaster.html')

def SignUpUser(request):
    if request.method == "POST":
        try:
            RetData = LoginUser.objects.filter(Q(UserId = request.POST.get('txtUserId')))
            if(RetData.count() > 0):
                ResponceStatus = "User Id Already Exists !!"
                return render(request,"SignUp.html",{'ResStatus': ResponceStatus})

            lognUser = LoginUser(UserId = request.POST.get('txtUserId'),
                Password = request.POST.get('txtCnfPassword'),
                CreatedBy = request.session['_UserId'],
                CreatedOn= str(datetime.date.today()),
                ModifiedBy= request.session['_UserId'],
                ModifiedOn= str(datetime.date.today()),
                isActive = 0)
            lognUser.save()
            _userLatestId = lognUser.pk #get the PK of the Record

            regUser = RegisterUser(FullName= request.POST.get('txtFullName'),
                Gender= request.POST.get('txtGender'),
                BloodGroup= request.POST.get('txtBldGrp'),
                MobileNo= request.POST.get('txtMoblieNumber'),
                Country= request.POST.get('txtCountry'),
                State= request.POST.get('txtState'),
                City= request.POST.get('txtCity'),
                PinCode= request.POST.get('txtPinCode'),
                EmailId= request.POST.get('txtEmailId'),
                UserID = _userLatestId)        
            regUser.save()
            ResponceStatus = "User Saved Successfully !!"
            return render(request,"SignUp.html",{'ResStatus': ResponceStatus})
        except Exception as e:
            ResponceStatus = "Error Occured in Form !!"
            return render(request,"SignUp.html",{'ResStatus': ResponceStatus})
    else:
        return render(request,"SignUp.html")

def UserHome(request):
    UsrId = request.session['_UserId']
    return render(request,'UserHome.html',{ 'UsrId' : UsrId })

#Donor Operation
def DonorList(request):
    ResponceStatus = ''
    PkUserId = request.session['_PkId']
    MaxRegId = random_number(5,5)
    if(request.session["UserRoleId"] == 1):
        Join_Query = DonorRegistration.objects.raw('''Select * from tbl_DonorList''')
    else:
        Join_Query = DonorRegistration.objects.raw('''Select * from tbl_DonorList where isActive=1''')
    return render(request,'dnrList.html',{ 'DonorListData' : Join_Query,'MyLatestId':MaxRegId,'ResponceStatus':ResponceStatus})

def DonorResg(request):
    MaxRegId = random_number(5,5)
    if request.method == "POST":
        try:
            dnrCreation = DonorRegistration(DonorRegNumber = request.POST.get('txtDnrRegNo'),
                FullName = request.POST.get('txtDnrName'),
                Address = request.POST.get('txtDnrAddress'),
                Gender = request.POST.get('ddlDnrGender'),
                Age = request.POST.get('txtAge'),
                DOB = request.POST.get('txtDob'),
                BloodGroup = request.POST.get('ddlBldGrp'),
                Weight = request.POST.get('txtWeight'),
                EmailId = request.POST.get('txtEmailId'),
                ContactNo = request.POST.get('txtMobNo'),
                LastDonated = request.POST.get('txtLstBldDon'),
                Country = request.POST.get('txtCountry'),
                State = request.POST.get('txtState'),
                City = request.POST.get('txtCity'),
                CreatedBy = request.session['_UserId'],
                CreatedOn= str(datetime.date.today()),
                ModifiedBy= request.session['_UserId'],
                ModifiedOn= str(datetime.date.today()),
                isActive = 0)
            dnrCreation.save()
            Join_Query = DonorRegistration.objects.raw('''Select * from tbl_DonorList''')
            ResponceStatus = "Donor Saved Successfully !!"
        except:
            ResponceStatus = "Something Went Wrong !!"

        return render(request,"dnrList.html",{'DonorListData' : Join_Query,'ResponceStatus': ResponceStatus,'MyLatestId' : MaxRegId})
    else:
        return render(request,"dnrList.html",{'MyLatestId' : MaxRegId })

def DeacDonor(request):
    DonorPkId = request.GET["DonorPkId"]
    Status = request.GET["Status"]
    Message = request.GET["Message"]
    MaxRegId = random_number(5,5)

    try:
        DonorData = DonorRegistration.objects.get(DnrRegId=DonorPkId)
        DonorData.isActive = Status
        DonorData.save()
        ResponceStatus = "Donor " + Message + " Successfully !!"

        recCnt = 1
        Join_Query = DonorRegistration.objects.raw('''Select * from tbl_DonorList''')
    except Exception as e:
        ResponceStatus = "Something went wrong !!"
        MaxRegId = request.GET.get('DnrRegNoHid')
    return render(request,'dnrList.html',{ 'DonorListData':Join_Query,'ResponceStatus' : ResponceStatus,'MyLatestId':MaxRegId})

def DeleteDonor(request):
    DonorPkId = request.GET["DonorPkId"]
    MaxRegId = random_number(5,5)

    try:
        DonorData = DonorRegistration.objects.get(DnrRegId=DonorPkId)
        DonorData .delete()
        ResponceStatus = "Donor Deleted Successfully !!"

        if(request.session["UserRoleId"] == 1):
            Join_Query = DonorRegistration.objects.raw('''Select * from tbl_DonorList''')
        else:
            Join_Query = DonorRegistration.objects.raw('''Select * from tbl_DonorList where isActive=1''')
    except Exception as e:
        ResponceStatus = "Something went wrong !!"
    return render(request,'dnrList.html',{ 'DonorListData':Join_Query,'ResponceStatus' : ResponceStatus,'MyLatestId':MaxRegId })

def DonorEdit(request):
    
    ResponceStatus = ""
    MaxRegId = random_number(5,5)

    try:
        if request.method == "POST":
            DonorPkId = request.POST.get('HidDonorPkId')
            DonorData = DonorRegistration.objects.get(DnrRegId=DonorPkId)

            DonorData.DonorRegNumber = request.POST.get('txtEditDnrRegNo')
            DonorData.FullName = request.POST.get('txtEditDnrName')
            DonorData.Address = request.POST.get('txtEditDnrAddress')
            DonorData.Gender = request.POST.get('ddlEditDnrGender')
            DonorData.Age = request.POST.get('txtEditAge')
            DonorData.DOB = request.POST.get('txtEditDob')
            DonorData.BloodGroup = request.POST.get('ddlEditBldGrp')
            DonorData.Weight = request.POST.get('txtEditWeight')
            DonorData.EmailId = request.POST.get('txtEditEmailId')
            DonorData.ContactNo = request.POST.get('txtEditMobNo')
            DonorData.LastDonated = request.POST.get('txtEditLstBldDon')
            DonorData.Country = request.POST.get('txtEditCountry')
            DonorData.State = request.POST.get('txtEditState')
            DonorData.City = request.POST.get('txtEditCity')
            DonorData.ModifiedBy = request.session['_UserId']
            DonorData.ModifiedOn = str(datetime.date.today())

            DonorData.save()
            DonorData = ""
            ResponceStatus = "Updated Successfully !!"
            StockData = ""
        else:
            DonorPkId = request.GET['DonorPkId']
            DonorData = DonorRegistration.objects.get(DnrRegId=DonorPkId)

        if(request.session["UserRoleId"] == 1):
            Join_Query = DonorRegistration.objects.raw('''Select * from tbl_DonorList''')
        else:
            Join_Query = DonorRegistration.objects.raw('''Select * from tbl_DonorList where isActive=1''')

    except Exception as e:
        ResponceStatus = "Something went wrong !!"
    return render(request,'dnrList.html',{ 'DonorListData':Join_Query,'ResponceStatus' : ResponceStatus,'MyLatestId':MaxRegId , 'DonorSpecificData':DonorData })

#End of Donor Registration
def SiteMaster(request):
    UsrId = request.session['_UserId']
    UserPkId = request.session['_PkId']

    UserImage = UsersImage.objects.filter(UserId = UserPkId)
    if(UserImage.count() > 0):
        UserImage = UsersImage.objects.filter(UserId = UserPkId).latest('ImageId')

    return render(request,'SiteMaster.html',{ 'UsrId' : UsrId, 'UserImage':UserImage })

#User Section
def random_number(min_char=5,max_char=8):
    allchar = string.ascii_letters.upper() + string.digits
    randNumber = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
    return randNumber

def GetUserDetail(request):
    recCnt = 1

    RoleList = GetUserRoleList(request)

    PkUserId = request.session['_PkId']
    Join_Query = LoginUser.objects.raw('''Select * from tbl_UserLogin,tbl_UserRegistration 
            where tbl_UserLogin.LogUserId = tbl_UserRegistration.UserID and tbl_UserLogin.LogUserId != ''' + str(request.session['_PkId']))
    personalDetail = RegisterUser.objects.all()
    return render(request,"UserDetail.html",{'UserData':Join_Query,'RecCnt':recCnt,'CurUserId':request.session['_PkId'],'UserRoleList':RoleList})

def AddUser(request):
    RoleList = ''
    try:
        RetData = LoginUser.objects.filter(Q(UserId = request.POST.get('UserId')))
        RoleList = GetUserRoleList(request)

        Join_Query = LoginUser.objects.raw('''Select * from tbl_UserLogin,tbl_UserRegistration 
            where tbl_UserLogin.LogUserId = tbl_UserRegistration.UserID and tbl_UserLogin.LogUserId != ''' + str(request.session['_PkId']))

        if(RetData.count() > 0):
            ResponceStatus = "User Id Already Exists !!"
            return render(request,"UserDetail.html",{'ResponceStatus': ResponceStatus,'UserData':Join_Query})

        lognUser = LoginUser(
                UserId = request.POST.get('UserId'),
                Password = request.POST.get('password'),
                UserRoleId = request.POST.get('UserRole'),
                CreatedBy = request.session['_UserId'],
                CreatedOn= str(datetime.date.today()),
                ModifiedBy= request.session['_UserId'],
                ModifiedOn= str(datetime.date.today()),
                isActive = 1)
        lognUser.save()
        _userLatestId = lognUser.pk #get the PK of the Record

        regUser = RegisterUser(FullName= request.POST.get('fullName'),
            Address = request.POST.get('address'),
            BloodGroup= request.POST.get('BldGrp'),
            Gender= request.POST.get('gender'),
            Country= request.POST.get('country'),
            State= request.POST.get('state'),
            City= request.POST.get('city'),
            PinCode= request.POST.get('pincode'),
            PersonInfo = request.POST.get('persInfo'),
            UserID = _userLatestId)        
        regUser.save()
        ResponceStatus = "User Saved Successfully !!"
        
        Join_Query = LoginUser.objects.raw('''Select * from tbl_UserLogin,tbl_UserRegistration 
            where tbl_UserLogin.LogUserId = tbl_UserRegistration.UserID and tbl_UserLogin.LogUserId != ''' + str(request.session['_PkId']))

    except Exception as e:
        ResponceStatus = "Something went wrong !!"
    return render(request,'UserDetail.html',{ 'ResponceStatus' : ResponceStatus,'UserData':Join_Query ,'UserRoleList':RoleList})

def CreateLoginHistory(LgUserId):
    lgnHist = LoginHistory(UserId = LgUserId,
                LoggedOn = str(datetime.datetime.now()))
    lgnHist.save()

def DeleteUser(request):
    UserPkId = request.GET["UserPkId"]
    RoleList = ''
    try:

        RoleList = GetUserRoleList(request)

        UserData = RegisterUser.objects.get(UserID=UserPkId)
        UserData .delete()

        LoginData = LoginUser.objects.get(LogUserId=UserPkId)
        LoginData.delete()
        ResponceStatus = "User Deleted Successfully !!"

        Join_Query = LoginUser.objects.raw('''Select * from tbl_UserLogin,tbl_UserRegistration 
            where tbl_UserLogin.LogUserId = tbl_UserRegistration.UserID and tbl_UserLogin.LogUserId != ''' + str(request.session['_PkId']))
    except Exception as e:
        ResponceStatus = "Something went wrong !!"
    return render(request,'UserDetail.html',{ 'ResponceStatus' : ResponceStatus,'UserData':Join_Query,'CurUserId':request.session['_PkId'],'UserRoleList':RoleList})

def DeacUser(request):
    UserPkId = request.GET["UserPkId"]
    Status = request.GET["Status"]
    Message = request.GET["Message"]
    RoleList = ''

    try:

        RoleList = GetUserRoleList(request)

        LoginData = LoginUser.objects.get(LogUserId=UserPkId)
        LoginData.isActive = Status
        LoginData.save()
        ResponceStatus = "User " + Message + " Successfully !!"

        Join_Query = LoginUser.objects.raw('''Select * from tbl_UserLogin,tbl_UserRegistration 
            where tbl_UserLogin.LogUserId = tbl_UserRegistration.UserID and tbl_UserLogin.LogUserId != ''' + str(request.session['_PkId']))
    except Exception as e:
        ResponceStatus = "Something went wrong !!"
    return render(request,'UserDetail.html',{ 'ResponceStatus' : ResponceStatus,'UserData':Join_Query,'CurUserId':request.session['_PkId'],'UserRoleList':RoleList})

def UserHistory(request):
    Join_Query = LoginHistory.objects.values("UserId").annotate(FirstLog=Min('LoggedOn')).annotate(LatstLog=Max('LoggedOn')).annotate(TtlLog=Count('UserId'))
    return render(request,'UserHistory.html',{ 'ResponceStatus' : Join_Query,'CurUserId':request.session['_PkId']})
#End User Section

#UserRole Section

def GetUserRoleList(request):

    RoleList = ''
    try:
        RoleList = UserRoles.objects.raw('''Select * from tbl_UserRole where isActive = 1''')
        ResponceStatus = "Successfully"
    except Exception as e:
        ResponceStatus = "Something Went Wrong"

    return RoleList

#UserRole End Section

#Blood Stock Detail
def StockMasterList(request):
    ResponceStatus = ''
    PkUserId = request.session['_PkId']
    MaxRegId = random_number(5,5)
    Join_Query = StockDetail.objects.raw('''Select * from tbl_StockDetail where isActive = 1''')
    return render(request,'StockMaster.html',{ 'StockListData' : Join_Query,'MyLatestId':MaxRegId,'ResponceStatus':ResponceStatus})

def StockMasterResg(request):
    if request.method == "POST":
        try:
            Join_Query = StockDetail.objects.raw('''Select * from tbl_StockDetail where isActive = 1''')
            isExist = StockDetail.objects.filter(Q(Sample = request.POST.get('ddlSamplType')))
            ResponceStatus = "Sample Already Registered !!"

            if(isExist.count() > 0):
                return render(request,"StockMaster.html",{'StockListData' : Join_Query,'ResponceStatus': ResponceStatus})

            StockCreation = StockDetail(Sample = request.POST.get('ddlSamplType'),
                Quantity = request.POST.get('QuantityTxt'),
                PurchasedOn = request.POST.get('PurchasedOn'),
                ExpireOn = request.POST.get('ExpiredOn'),
                CreatedBy = request.session['_UserId'],
                CreatedOn= str(datetime.date.today()),
                ModifiedBy= request.session['_UserId'],
                ModifiedOn= str(datetime.date.today()),
                isActive =1)
            StockCreation.save()
            ResponceStatus = "Sample Saved Successfully !!"
        except:
            ResponceStatus = "Something Went Wrong !!"

        return render(request,"StockMaster.html",{'StockListData' : Join_Query,'ResponceStatus': ResponceStatus})
    else:
        MaxRegId = random_number(5,5)
        return render(request,"StockMaster.html",{'MyLatestId' : MaxRegId })

def StockMasterDeac(request):
    SmpPkId = request.GET["SmpPkId"]
    Status = request.GET["Status"]
    Message = request.GET["Message"]
    MaxRegId = random_number(5,5)

    try:
        StockData = StockDetail.objects.get(StockId=SmpPkId)
        StockData.isActive = Status
        StockData.save()
        ResponceStatus = "Sample " + Message + " Successfully !!"

        recCnt = 1
        Join_Query = StockDetail.objects.raw('''Select * from tbl_StockDetail where isActive = 1''')
    except Exception as e:
        ResponceStatus = "Something went wrong !!"
    return render(request,'StockMaster.html',{ 'StockListData':Join_Query,'ResponceStatus' : ResponceStatus})

def StockMasterDelete(request):
    SmplePkId = request.GET["SmpPkId"]

    try:
        StockData = StockDetail.objects.get(StockId=SmplePkId)
        StockData.delete()
        ResponceStatus = "Sample Deleted Successfully !!"

        recCnt = 1
        Join_Query = StockDetail.objects.raw('''Select * from tbl_StockDetail where isActive = 1''')
    except Exception as e:
        ResponceStatus = "Something went wrong !!"
    return render(request,'StockMaster.html',{ 'StockListData':Join_Query,'ResponceStatus' : ResponceStatus})

def StockMasterEdit(request):
    
    PkUserId = request.session['_PkId']
    ResponceStatus = ""

    #StockPkId

    try:
        if request.method == "POST":
            SmplePkId = request.POST.get('HidStockPkId')
            StockData = StockDetail.objects.get(StockId=SmplePkId)

            StockData.Sample = str(request.POST.get('ddlEditSmpleType'))
            StockData.Quantity = request.POST.get('EditQuantity')
            StockData.PurchasedOn = str(request.POST.get('EditPurchasedOn'))
            StockData.ExpireOn = str(request.POST.get('EditExpiredOn'))
            StockData.ModifiedBy = str(request.session['_UserId'])
            StockData.ModifiedOn = str(datetime.date.today())

            StockData.save()
            ResponceStatus = "Updated Successfully !!"
            StockData = ""
        else:
            SmplePkId = request.GET["SmpPkId"]
            StockData = StockDetail.objects.get(StockId=SmplePkId)
        Join_Query = StockDetail.objects.raw('''Select * from tbl_StockDetail where isActive = 1''')
    except Exception as e:
        ResponceStatus = "Something went wrong !!"
    return render(request,'StockMaster.html',{ 'StockListData' : Join_Query,'SpecificData':StockData,'ResponceStatus' : ResponceStatus})

#End of Blood Stock Detail


#Contact Us
def ContactUsMaster(request):
    try:
        ResponceStatus = ""
        if(request.method == "POST"):

            SaveCntact = ContactUs(Name = request.POST.get("firstName") + " " + request.POST.get("lastName"),
                Email = request.POST.get("emailId"),
                ContactNo = request.POST.get("contactNo"),
                Comments= request.POST.get("Message"),
                Suggestion = request.POST.get("Suggestion"),
                PostedOn = str(datetime.date.today()),
                isActive = 1)
            SaveCntact.save()
            ResponceStatus = "Message Sent Successfully !!"

            #subject = 'Thank you for registering to our site'
            #message = request.POST.get('txtMessage')
            #email_from = request.POST.get('txtEmailId')
            #email_to = [settings.EMAIL_HOST_USER]

            #send_mail(subject, message, email_from, email_to)
    except Exception as e:
        ResponceStatus = "Something went wrong !!"

    return render(request,"ContactUs.html",{"ResponceStatus":ResponceStatus})

def CommentList(request):
    try:
        if(request.method == "POST"):
            sasd = ""
        else:
            Join_Query = ContactUs.objects.raw('''Select * from tbl_contactUs''')
            ResponceStatus = ''
    except Exception as e:
        ResponceStatus = "Something wrong !!"
    return render(request,'CommentList.html',{'ResponceStatus':ResponceStatus,'MessageList':Join_Query})

def DeleteCmt(request):
    CommentPkId = request.GET["CommentPkId"]
    Message = request.GET["Message"]

    try:
        CommentData = ContactUs.objects.get(ContactPkId=CommentPkId)
        CommentData .delete()
        ResponceStatus = "Comment " + Message + " Successfully !!"
        Join_Query = ContactUs.objects.raw('''Select * from tbl_contactUs''')
    except Exception as e:
        ResponceStatus = "Something went wrong !!"
    return render(request,'CommentList.html',{'ResponceStatus':ResponceStatus,'MessageList':Join_Query})

def HideCmt(request):
    CommentPkId = request.GET["CommentPkId"]
    Message = request.GET["Message"]
    Status = request.GET["Status"]

    try:
        CommentData = ContactUs.objects.get(ContactPkId=CommentPkId)
        CommentData.isActive = Status
        CommentData.save()

        ResponceStatus = "Comment " + Message + " Successfully !!"
        Join_Query = ContactUs.objects.raw('''Select * from tbl_contactUs''')
    except Exception as e:
        ResponceStatus = "Something went wrong !!"
    return render(request,'CommentList.html',{'ResponceStatus':ResponceStatus,'MessageList':Join_Query})
#End of Contact Us
    
#User Profile
def ImagetoBase64(ImagePath):
    imageString = ""
    with open(ImagePath, "rb") as imageFile:
        imageString = base64.b64encode(imageFile.read())
    return imageString

def EditProfile(request):
    UserPkId = request.session['_PkId']
    try:
        UserData = RegisterUser.objects.get(UserID = UserPkId)
        UserImage = UsersImage.objects.filter(UserId = UserPkId)
        if(UserImage.count() > 0):
            UserImage = UsersImage.objects.filter(UserId = UserPkId).latest('ImageId')
    
        ResponceStatus = ""

        if request.method == "POST":

            UserData.FullName = request.POST.get('fullname')
            if(request.POST.get('contactNo') != ""):
                UserData.MobileNo = request.POST.get('contactNo')
            else:
                UserData.MobileNo = 0

            if(request.POST.get('emailId') != ""):
                UserData.EmailId = request.POST.get('emailId')
            else:
                UserData.EmailId = ''

            UserData.Gender = request.POST.get('gender')
            UserData.BloodGroup = request.POST.get('bloodgroup')
            UserData.Address = request.POST.get('address')
            UserData.City = request.POST.get('city')
            UserData.State = request.POST.get('state')
            UserData.Country = request.POST.get('country')

            UserData.save()


            if (request.POST.get("UserProfImg") != ""):
                ImgUpld = UsersImage(UserId = request.session['_PkId'],
                    ImageBase64String = request.POST.get("UserProfImg"),
                    ImageName = request.POST.get('ImageName'),
                    ImageType = "ProfilePic",
                    UpdatedOn = str(datetime.date.today()))
                ImgUpld.save()
            #Fetching Latest Data
            UserData = RegisterUser.objects.get(UserID = UserPkId)
            UserImage = UsersImage.objects.filter(UserId = UserPkId)
            if(UserImage.count() > 0):
                UserImage = UsersImage.objects.filter(UserId = UserPkId).latest('ImageId')
            #Fetching Latest Data
            ResponceStatus = "Detail Updated Successsfully !!"
    except Exception as e:
        ResponceStatus = "Something went wrong !!"
    return render(request,"UserProfile.html",{"UserData":UserData,"UserImage":UserImage,"ResponceStatus":ResponceStatus})
#End of User Profile

#User ChnagePassword
def ChangePassword(request):

    try:
        ResponceStatus = ''
        if request.method == "GET":
            LoginDetail = LoginUser.objects.get(UserId = request.session["_UserId"])
            EncryptPassword = str(base64.b64encode(LoginDetail.Password.encode()))[2:-1]
        else:
            LoginDetail = LoginUser.objects.get(UserId = request.session["_UserId"])
            LoginDetail.Password = request.POST.get('newPassword')
            LoginDetail.ModifiedOn = str(datetime.date.today())
            LoginDetail.save()
            EncryptPassword = str(base64.b64encode(LoginDetail.Password.encode()))[2:-1]
            ResponceStatus = "Password Updated Successfully !!"

    except Exception as e:
        ResponceStatus = "Something went wrong !!"
    return render(request,'ChangePassword.html',{"EncryptPassword":EncryptPassword,'ResponceStatus':ResponceStatus})

def ForgotPassword(request):

    try:
        ResponceStatus = ''
        if request.method == "POST":
            try:
                LoginDetail = LoginUser.objects.get(UserId = request.POST.get("UserID"))
                LoginDetail.Password = request.POST.get('password')
                LoginDetail.ModifiedOn = str(datetime.date.today())
                LoginDetail.save()
                ResponceStatus = "Password Changed Successfully !!"
            except LoginUser.DoesNotExist as e:
                ResponceStatus = "Wrong User Id !!"
            
    except Exception as e:
        ResponceStatus = "Something went wrong !!"

    return render(request,'ForogtPassword.html',{'ResponceStatus':ResponceStatus})

#End of ChangePassword

#Mail Operations
def MailHomeMaster(request):

    UserMailId = RegisterUser.objects.get(UserID = request.session["_PkId"])
    ttlMailReceive = MailMaster.objects.filter(SentTo = UserMailId.EmailId)
    ttlMailSent = MailMaster.objects.filter(From = UserMailId.EmailId)
    #for MailRecItem in ttlMailReceive:
    #    MailRecItem.SentOn = MailRecItem.SentOn.strftime("%H : %M : %S %p")

    #ttlMailSent = MailMaster.objects.filter(From = UserMailId.EmailId)
    #for MailSentItem in ttlMailSent:
    #    MailSentItem.SentOn = MailSentItem.SentOn.strftime("%H : %M : %S %p")

    return render(request,"MailMaster.html",{'MailSent':ttlMailSent,'MailSentCnt':ttlMailSent.count(),'MailRecieved':ttlMailReceive,'MailReceivedCnt':ttlMailReceive.count()})

def MailSentMaster(request):
    try:
        UserMailId = RegisterUser.objects.get(UserID = request.session["_PkId"])

        UserMailId = RegisterUser.objects.get(UserID = request.session["_PkId"])
        ttlMailReceive = MailMaster.objects.filter(SentTo = UserMailId.EmailId)
        ttlMailSent = MailMaster.objects.filter(From = UserMailId.EmailId)

        Mail_Sent = MailMaster(SentTo = request.POST.get("mailToHidden"),
            CcAcnt = request.POST.get("mailCcHidden"),
            BccAcnt = request.POST.get("mailBCCHidden"),
            Subject = request.POST.get("mailSubjectTxt"),
            Message = request.POST.get("messageHid"),
            From = UserMailId.EmailId,
            SentOn = str(datetime.datetime.now()),
            isDelivered = 1,
            CreatedOn = str(datetime.datetime.now()),
            CreatedBy = request.session["_PkId"],
            ModifiedOn = str(datetime.datetime.now()),
            ModifiedBy = request.session["_PkId"])
        Mail_Sent.save()

        ResponceStatus = "Mail Sent Successfully !!"
    except Exception as e:
        ResponceStatus = "Something Went Wrong !!"
    return render(request,"MailMaster.html",{'ResponceStatus':ResponceStatus,'MailSent':ttlMailSent,'MailSentCnt':ttlMailSent.count(),'MailRecieved':ttlMailReceive,'MailReceivedCnt':ttlMailReceive.count()})

#End of Mail Operation


#Send Mail
#def SendEmail(request,Subject,Message,MailFrom):

#    mailObj = MIMEMultipart()
#    mailObj["From"] = Email
#    mailObj["Subject"] = Subject
#    mailObj["To"] = Subject

#    return ""
#End of Send Mail
