
from django.shortcuts import render, redirect
import uuid
import datetime
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q

from django.core.mail import send_mail
from django.conf import settings

#Email Library
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#End of Email Library
from django.http import HttpResponse
from django.template import loader
from django.db.models import *
import string
from random import *
import base64

# Create your views here.
from AppComponent.models import LoginUser
from AppComponent.models import RegisterUser
from AppComponent.models import DonorRegistration
from AppComponent.models import StockDetail
from AppComponent.models import LoginHistory
from AppComponent.models import ContactUs
from AppComponent.models import UsersImage
from AppComponent.models import MailMaster
from AppComponent.models import SaveMailMaster
from AppComponent.models import UserRoles
from AppComponent.models import BloodRquestMaster
from AppComponent.models import TupleList
  
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
    UserPkId = request.session['_PkId']

    UserMailId = RegisterUser.objects.get(UserID = request.session["_PkId"])
    CurrentUseRoleId = request.session['UserRoleId']
    DashBoardListItem = []


    if CurrentUseRoleId == 1:
        ttlUsers = LoginUser.objects.all()
        ttlActiveUser = LoginUser.objects.filter(isActive = 1)
        ttlUnActiveUser = LoginUser.objects.filter(isActive = 0)

        UserDetail = TupleList()
        UserDetail.Title = "Users : "
        UserDetail.ClassName = "col-md-3 col-sm-6"
        UserDetail.DisplayIcon = "fa fa-users"
        UserDetail.ActiveLstCap = "Active : "
        UserDetail.InActiveLstCap = "In-Active : "
        UserDetail.TtlCount = ttlUsers.count()
        UserDetail.TtlActiveCount = ttlActiveUser.count()
        UserDetail.TtlInActiveCount = ttlUnActiveUser.count()
        DashBoardListItem.append(UserDetail)

    elif CurrentUseRoleId == 2:
        #ttlMailMast = MailMaster.objects.all()
        ttlMailMastInbox = MailMaster.objects.filter(SentTo = UserMailId.EmailId)
        ttlMailMastSent = MailMaster.objects.filter(From = UserMailId.EmailId)
        ttlMailMast = ttlMailMastInbox.count() + ttlMailMastSent.count()

        MailMasterList = TupleList()
        MailMasterList.Title = "Mail : "
        MailMasterList.ClassName = "col-md-3 col-sm-6"
        MailMasterList.DisplayIcon = "fa fa-envelope-o"
        MailMasterList.ActiveLstCap = "Recieved : "
        MailMasterList.InActiveLstCap = "Sent : "
        MailMasterList.TtlCount = ttlMailMast
        MailMasterList.TtlActiveCount = ttlMailMastInbox.count()
        MailMasterList.TtlInActiveCount = ttlMailMastSent.count()
        DashBoardListItem.append(MailMasterList)

    elif CurrentUseRoleId == 3:
        ttlMailMast = MailMaster.objects.all()
        ttlMailMastInbox = MailMaster.objects.filter(SentTo = UserMailId.EmailId)
        ttlMailMastSent = MailMaster.objects.filter(From = UserMailId.EmailId)

        MailMasterList = TupleList()
        MailMasterList.Title = "Mail : "
        MailMasterList.ClassName = "col-md-6 col-sm-6"
        MailMasterList.DisplayIcon = "fa fa-envelope-o"
        MailMasterList.ActiveLstCap = "Recieved : "
        MailMasterList.InActiveLstCap = "Sent : "
        MailMasterList.TtlCount = ttlMailMast.count()
        MailMasterList.TtlActiveCount = ttlMailMastInbox.count()
        MailMasterList.TtlInActiveCount = ttlMailMastSent.count()
        DashBoardListItem.append(MailMasterList)

        ttlBloodRequest = BloodRquestMaster.objects.filter(UserId = UserPkId)
        ttlPendingBldReq = BloodRquestMaster.objects.filter(Q(isActive = 1) & Q(UserId = UserPkId))
        ttlUnActiveBldReq = BloodRquestMaster.objects.filter(Q(isActive = 0) & Q(UserId = UserPkId))

        BloodRequest = TupleList()
        BloodRequest.Title = "Blood-Request : "
        BloodRequest.ClassName = "col-md-6 col-sm-6"
        BloodRequest.DisplayIcon = "fa fa-tint"
        BloodRequest.ActiveLstCap = "Active : "
        BloodRequest.InActiveLstCap = "In-Active : "
        BloodRequest.TtlCount = ttlBloodRequest.count()
        BloodRequest.TtlActiveCount = ttlPendingBldReq.count()
        BloodRequest.TtlInActiveCount = ttlUnActiveBldReq.count()
        DashBoardListItem.append(BloodRequest)

    if CurrentUseRoleId == 1 or CurrentUseRoleId == 2:
        ttlDonors = DonorRegistration.objects.all()
        ttlActiveDonors = DonorRegistration.objects.filter(isActive = 1)
        ttlUnActiveDonor = DonorRegistration.objects.filter(isActive = 0)

        DonorDetail = TupleList()
        DonorDetail.Title = "Donor : "
        DonorDetail.ClassName = "col-md-3 col-sm-6"
        DonorDetail.DisplayIcon = "fa fa-beer"
        DonorDetail.ActiveLstCap = "Active : "
        DonorDetail.InActiveLstCap = "In-Active : "
        DonorDetail.TtlCount = ttlDonors.count()
        DonorDetail.TtlActiveCount = ttlActiveDonors.count()
        DonorDetail.TtlInActiveCount = ttlUnActiveDonor.count()
        DashBoardListItem.append(DonorDetail)

        ttlStock = StockDetail.objects.all()
        ttlActiveStock = StockDetail.objects.filter(isActive = 1)
        ttlExpiredStock = StockDetail.objects.filter(isActive = 0)

        StockDetailData = TupleList()
        StockDetailData.Title = "Stock : "
        StockDetailData.ClassName = "col-md-3 col-sm-6"
        StockDetailData.DisplayIcon = "fa fa-cubes"
        StockDetailData.ActiveLstCap = "Active : "
        StockDetailData.InActiveLstCap = "In-Active : "
        StockDetailData.TtlCount = ttlStock.count()
        StockDetailData.TtlActiveCount = ttlActiveStock.count()
        StockDetailData.TtlInActiveCount = ttlExpiredStock.count()
        DashBoardListItem.append(StockDetailData)

        ttlBloodRequest = BloodRquestMaster.objects.all()
        ttlPendingBldReq = BloodRquestMaster.objects.filter(isActive = 1)
        ttlUnActiveBldReq = BloodRquestMaster.objects.filter(isActive = 0)

        BloodRequest = TupleList()
        BloodRequest.Title = "Blood-Request : "
        BloodRequest.ClassName = "col-md-3 col-sm-6"
        BloodRequest.DisplayIcon = "fa fa-tint"
        BloodRequest.ActiveLstCap = "Active : "
        BloodRequest.InActiveLstCap = "In-Active : "
        BloodRequest.TtlCount = ttlBloodRequest.count()
        BloodRequest.TtlActiveCount = ttlPendingBldReq.count()
        BloodRequest.TtlInActiveCount = ttlUnActiveBldReq.count()
        DashBoardListItem.append(BloodRequest)

    return render(request,'UserHome.html',{ 'UsrId' : UsrId , 'DashBoardListItem' : DashBoardListItem, 'BloodRequest' : ttlBloodRequest })

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

        lognUser = LoginUser(UserId = request.POST.get('UserId'),
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
    if(request.session['UserRoleId'] != 3):
        Join_Query = StockDetail.objects.raw('''Select * from tbl_StockDetail''')
    else:
        Join_Query = StockDetail.objects.raw('''Select * from tbl_StockDetail where isActive=1''')
    return render(request,'StockMaster.html',{ 'StockListData' : Join_Query,'MyLatestId':MaxRegId,'ResponceStatus':ResponceStatus})

def StockMasterResg(request):
    if request.method == "POST":
        try:
            if(request.session['UserRoleId'] != 3):
                Join_Query = StockDetail.objects.raw('''Select * from tbl_StockDetail''')
            else:
                Join_Query = StockDetail.objects.raw('''Select * from tbl_StockDetail where isActive=1''')
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
        if(request.session['UserRoleId'] != 3):
            Join_Query = StockDetail.objects.raw('''Select * from tbl_StockDetail''')
        else:
            Join_Query = StockDetail.objects.raw('''Select * from tbl_StockDetail where isActive=1''')
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
        if(request.session['UserRoleId'] != 3):
            Join_Query = StockDetail.objects.raw('''Select * from tbl_StockDetail''')
        else:
            Join_Query = StockDetail.objects.raw('''Select * from tbl_StockDetail where isActive=1''')
    except Exception as e:
        ResponceStatus = "Something went wrong !!"
    return render(request,'StockMaster.html',{ 'StockListData':Join_Query,'ResponceStatus' : ResponceStatus})

def StockMasterEdit(request):
    
    PkUserId = request.session['_PkId']
    ResponceStatus = ""
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
        if(request.session['UserRoleId'] != 3):
            Join_Query = StockDetail.objects.raw('''Select * from tbl_StockDetail''')
        else:
            Join_Query = StockDetail.objects.raw('''Select * from tbl_StockDetail where isActive=1''')
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
    ttlMailSaved = SaveMailMaster.objects.filter(UserId = UserMailId.UserID)
    
    return render(request,"MailMaster.html",{'MailSent':ttlMailSent,'MailSentCnt':ttlMailSent.count(),'MailRecieved':ttlMailReceive,'MailReceivedCnt':ttlMailReceive.count(),'MailsSaved':ttlMailSaved,'MailSavedCount':ttlMailSaved.count()})

def MailSentMaster(request):
    try:

        MailMode = request.POST.get("MailModeHid")
        if MailMode == '2':
            return MailDraftMaster(request)

        UserMailId = RegisterUser.objects.get(UserID = request.session["_PkId"])
        ttlMailReceive = MailMaster.objects.filter(SentTo = UserMailId.EmailId)
        ttlMailSent = MailMaster.objects.filter(From = UserMailId.EmailId)
        ttlMailSaved = SaveMailMaster.objects.filter(UserId = UserMailId.UserID)

        Mail_Sent = MailMaster(SentTo = request.POST.get("mailToTxt"),
            CcAcnt = request.POST.get("mailCCtxt"),
            BccAcnt = request.POST.get("mailBcctxt"),
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

        ttlMailReceive = MailMaster.objects.filter(SentTo = UserMailId.EmailId)
        ttlMailSent = MailMaster.objects.filter(From = UserMailId.EmailId)
        ttlMailSaved = SaveMailMaster.objects.filter(UserId = UserMailId.UserID)

        ResponceStatus = "Mail Sent Successfully !!"
    except Exception as e:
        ResponceStatus = "Something Went Wrong !!"
    return render(request,"MailMaster.html",{'ResponceStatus':ResponceStatus,'MailSent':ttlMailSent,'MailSentCnt':ttlMailSent.count(),'MailRecieved':ttlMailReceive,'MailReceivedCnt':ttlMailReceive.count(),'MailsSaved':ttlMailSaved,'MailSavedCount':ttlMailSaved.count()})

def MailDraftMaster(request):
    try:
        UserMailId = RegisterUser.objects.get(UserID = request.session["_PkId"])
        ttlMailReceive = MailMaster.objects.filter(SentTo = UserMailId.EmailId)
        ttlMailSent = MailMaster.objects.filter(From = UserMailId.EmailId)
        ttlMailSaved = SaveMailMaster.objects.filter(UserId = UserMailId.UserID)

        DraftMail = SaveMailMaster(SentTo = request.POST.get("mailToTxt"),
                        CcAcnt = request.POST.get("mailCCtxt"),
                        BccAcnt = request.POST.get("mailBcctxt"),
                        Subject = request.POST.get("mailSubjectTxt"),
                        Message = request.POST.get("messageHid"),
                        From = UserMailId.EmailId,
                        UserId = UserMailId.UserID,
                        CreatedOn = str(datetime.datetime.now()),
                        CreatedBy = request.session["_PkId"],
                        ModifiedOn = str(datetime.datetime.now()),
                        ModifiedBy = request.session["_PkId"],
                        isActive = 1)
        DraftMail.save()

        ttlMailReceive = MailMaster.objects.filter(SentTo = UserMailId.EmailId)
        ttlMailSent = MailMaster.objects.filter(From = UserMailId.EmailId)
        ttlMailSaved = SaveMailMaster.objects.filter(UserId = UserMailId.UserID)
        ResponceStatus = "Mail Saved Successfully !!"
    except Exception as e:
        ResponceStatus = "Something Went Wrong !!"
    return render(request,"MailMaster.html",{'ResponceStatus':ResponceStatus,'MailSent':ttlMailSent,'MailSentCnt':ttlMailSent.count(),'MailRecieved':ttlMailReceive,'MailReceivedCnt':ttlMailReceive.count(),'MailsSaved':ttlMailSaved,'MailSavedCount':ttlMailSaved.count()})

def GetMailMessage(request):
    try:
        MailCurId = request.GET["MailPkId"]
        MailType = request.GET["MailType"]

        if MailType == '1' or MailType == '2':
            MailMast = MailMaster.objects.filter(PkId = MailCurId)

            CurMailInst = MailMaster.objects.get(PkId = MailCurId)
            CurMailInst.isRead = 1
            CurMailInst.save()
        else:
            MailMast = SaveMailMaster.objects.filter(PkId = MailCurId)

        MailMast_Json = serializers.serialize('json', MailMast)

        return HttpResponse(MailMast_Json)

    except Exception as e:
        return HttpResponse(e)
    

    #MailCurId

#End of Mail Operation

#Request Blood Master
def RequestBlood(request):
    ResponceStatus = ""
    try:
        if request.method == "POST":
            DyUniqueCode = str(DynUniqueCode(10))            
            BldReqMast = BloodRquestMaster(BloodType = request.POST.get("ddlBldGrp"),
                            Gender = request.POST.get("ddlGender"),
                            Quantity = request.POST.get("QuantityTxt"),
                            DeliverDate = request.POST.get("DeliverdBy"),
                            UniqueCode = DyUniqueCode,
                            UserId = request.session["_PkId"],
                            ReqStatus = "Pending",
                            CreatedBy = request.session['_UserId'],
                            ModifiedBy = request.session['_UserId'])
            BldReqMast.save()
            ResponceStatus = "Request Submitted Successfully !!<br/><br/>Request No.: " + DyUniqueCode

            MailMessage = "Your Request for Blood Request is Submitted Successfully !!\n\nRequest No.: " + DyUniqueCode
            isMailSent = SendEmail(request,"Blood Request",MailMessage,request.POST.get("EmailId"))
            if(isMailSent):
                ResponceStatus = ResponceStatus + "<br/><br/>Mail Sent Successfully !!"
            else:
                ResponceStatus = ResponceStatus + "<br/><br/>Error Occurred While Sending Mail !!"
    except Exception as e:
        ResponceStatus = "Something Went Wrong !!"

    UserDetail = RegisterUser.objects.get(UserID = request.session["_PkId"])
    return render(request,'RequestBlood.html',{'UserDetail':UserDetail,'ResponceStatus':ResponceStatus})

def RequestStatus(request):
    try:
        ResponceStatus = ""
        UserDetail = None
        UniqueCodeStatus = None
        BloodRequestStatus = None
        isFound = 0
        if request.method == "POST":
            UniqueCode = request.POST.get("UniqueCode")
            try:
                BloodRequestStatus = BloodRquestMaster.objects.get(UniqueCode = UniqueCode)
                UserDetail = RegisterUser.objects.get(UserID = BloodRequestStatus.UserId)
                isFound = 1
            except BloodRquestMaster.DoesNotExist as e:
                ResponceStatus = "Request Not Found !!"
    except Exception as e:
        ResponceStatus = "Something Went Wrong !!"
    return render(request,'RequestBloodStatus.html',{'ResponceStatus':ResponceStatus,'BloodRequestStatus':BloodRequestStatus,'UserDetail':UserDetail,'IsFound':isFound})

def BloodReqList(request):
    ResponceStatus = ""
    BloodRequestList = None
    try:
        try:
            UniqueCode = request.GET["UniqueCode"]
            StatusTo = request.GET["StatusTo"]
            ActiveState = request.GET["ActiveState"]
            Message = request.GET["Message"]

            BloodDetail = BloodRquestMaster.objects.get(UniqueCode = UniqueCode)
            BloodDetail.ReqStatus = StatusTo
            BloodDetail.isActive = ActiveState
            BloodDetail.save()

            ResponceStatus = Message
            BloodRequestList = BloodRquestMaster.objects.all()

            CurUserDetail = RegisterUser.objects.get(UserID = request.session["_PkId"])
            DestUserDetail = RegisterUser.objects.get(UserID = BloodDetail.UserId)
            
            #Save to MailBox
            Mail_Sent = MailMaster(SentTo = DestUserDetail.EmailId,
                CcAcnt = "",
                BccAcnt = "",
                Subject = "Blood Status",
                Message = "Blood Request : <u><b>" + UniqueCode + " has been declined.\n\n",
                From = CurUserDetail.EmailId,
                SentOn = str(datetime.datetime.now()),
                isDelivered = 1,
                CreatedOn = str(datetime.datetime.now()),
                CreatedBy = request.session["_PkId"],
                ModifiedOn = str(datetime.datetime.now()),
                ModifiedBy = request.session["_PkId"])
            Mail_Sent.save()

            UserId = RegisterUser.objects.get(UserID  = BloodDetail.UserId)
            if UserId.EmailId != "":
                MailMessage = "Blood Request : <u><b>" + UniqueCode + " has been declined.\n\n"
                MailMessage = MailMessage + "Reason: Blood Not Avilable"
                MailStatus = SendEmail(request,"Blood Request Status",MailMessage,UserId.EmailId)
                if(MailStatus == False):
                    ResponceStatus = ResponceStatus + "\n\nMail Not Sent"

        except Exception as e:
            BloodRequestList = BloodRquestMaster.objects.all()
    except Exception as e:
        ResponceStatus = "Internal Server Error !!"
    return render(request,'RequestBloodList.html',{'ResponceStatus':ResponceStatus,'BloodRequestList':BloodRequestList})

def BloodReqEdit(request):
    try:
        ResponceStatus = ""

        if request.method == "GET":
            BldReqId = request.GET["BldreqId"]
            BldReqDetail = BloodRquestMaster.objects.filter(PkId = BldReqId)
            BldReqDetail_Result = serializers.serialize('json', BldReqDetail)
            return HttpResponse(BldReqDetail_Result)
        else:
            BldReqId = request.POST.get('BldReqCode')
            BldReqDetail = BloodRquestMaster.objects.get(PkId = BldReqId)
            BldReqDetail.BloodType = request.POST.get('BldType')
            BldReqDetail.Gender = request.POST.get('bldReqFor')
            BldReqDetail.Quantity = request.POST.get('bldQuantity')
            BldReqDetail.DeliverDate = request.POST.get('bldDelDate')
            BldReqDetail.save()
            ResponceStatus = "Detail Updated Successfully !!"
            return HttpResponse(ResponceStatus)

    except Exception as e:
        ResponceStatus = "Internal Server Exception !!"
        return HttpResponse(ResponceStatus)


#Request Blood Master


#Send Mail
def SendEmail(request,Subject,Message,MailTo):
    IsMailSent = True
    try:
        #Create Mail Body
        MailMessage = MIMEMultipart() 
        MailMessage['From'] = settings.EMAIL_HOST_USER
        MailMessage['To'] = MailTo
        MailMessage['Subject'] = Subject
        MailMessage.attach(MIMEText(Message, 'plain'))

        #Send Mail Securly
        MailInstance = smtplib.SMTP(settings.EMAIL_HOST,settings.EMAIL_PORT)
        MailInstance.ehlo()
        MailInstance.starttls()
        MailInstance.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
        MailInstance.send_message(MailMessage)
        MailInstance.close()
    except Exception as e:
        IsMailSent = False
    return IsMailSent
#End of Send Mail

#Generate UniqeCode String
def DynUniqueCode(string_length):
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace("-","")
    return random[0:string_length]
