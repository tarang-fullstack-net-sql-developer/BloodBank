from __future__ import unicode_literals  
from django.db import models  
  
class Student(models.Model):  
    first_name = models.CharField(max_length=20)  
    last_name = models.CharField(max_length=30)  
    class Meta:  
        db_table = "student"

class Admins(models.Model):
    AdminId = models.AutoField(primary_key=True)
    UserId = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)
    CreatedBy = models.CharField(max_length=20)
    CreatedOn = models.CharField(max_length=20)
    ModifiedBy = models.CharField(max_length=20)
    ModifiedOn = models.CharField(max_length=20)
    isActive = models.BooleanField()
    class Meta:
        db_table = "tbl_Admin"


class LoginUser(models.Model):
    LogUserId = models.AutoField(primary_key=True)
    UserId = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)
    CreatedBy = models.CharField(max_length=20)
    CreatedOn = models.CharField(max_length=20)
    ModifiedBy = models.CharField(max_length=20)
    ModifiedOn = models.CharField(max_length=20)
    isActive = models.BooleanField(default=0)
    class Meta:
        db_table = "tbl_UserLogin"

class RegisterUser(models.Model):
    RegUserId = models.AutoField(primary_key=True)
    FullName = models.CharField(default="",max_length=50)
    Gender = models.CharField(default="",max_length=8)
    Address = models.CharField(default="",max_length=100)
    BloodGroup = models.CharField(default="",max_length=10)
    MobileNo = models.BigIntegerField(default=0)
    Country = models.CharField(default="",max_length=20)
    State = models.CharField(default="",max_length=20)
    City = models.CharField(default="",max_length=20)
    PinCode = models.BigIntegerField(default=0)
    PersonInfo = models.CharField(default="",max_length=250)
    EmailId = models.EmailField(default="")
    UserID = models.BigIntegerField(default=0)
    class Meta:
        db_table = "tbl_UserRegistration"

class DonorRegistration(models.Model):
    DnrRegId = models.AutoField(primary_key=True)
    DonorRegNumber = models.CharField(max_length=50)
    FullName = models.CharField(max_length=50)
    Address = models.CharField(max_length=50,null=True)
    Gender = models.CharField(max_length=50)
    Age = models.CharField(max_length=50,null=True)
    DOB = models.CharField(max_length=50,null=True)
    BloodGroup = models.CharField(max_length=50)
    LastDonated = models.CharField(max_length=50,null=True)
    ContactNo = models.BigIntegerField(null=True)
    State = models.CharField(max_length=50,null=True)
    City = models.CharField(max_length=50,null=True)
    Country = models.CharField(max_length=50,null=True)
    EmailId = models.EmailField(null=True)
    Weight = models.BigIntegerField(null=True)
    CreatedBy = models.CharField(max_length=20)
    CreatedOn = models.CharField(max_length=20)
    ModifiedBy = models.CharField(max_length=20)
    ModifiedOn = models.CharField(max_length=20)
    isActive = models.BooleanField(default=0)
    class Meta:
        db_table = "tbl_DonorList"

class StockDetail(models.Model):
    StockId = models.AutoField(primary_key=True)
    Sample = models.CharField(max_length=50)
    Quantity = models.BigIntegerField()
    PurchasedOn = models.CharField(max_length=20)
    ExpireOn = models.CharField(max_length=20)
    CreatedBy = models.CharField(max_length=20)
    CreatedOn = models.CharField(max_length=20)
    ModifiedBy = models.CharField(max_length=20)
    ModifiedOn = models.CharField(max_length=20)
    isActive = models.BooleanField(default=0)
    class Meta:
        db_table = "tbl_StockDetail"

class ContactInfo(models.Model):
    ContactId = models.AutoField(primary_key=True)
    FullName = models.CharField(max_length=50)
    EmailId = models.EmailField()
    ContactNo = models.BigIntegerField()
    Message = models.CharField(max_length=250)
    CreatedBy = models.CharField(max_length=20)
    CreatedOn = models.CharField(max_length=20)
    class Meta:
        db_table = "tbl_ContactDetail"
    
class BloodSmpReports(models.Model):
    RepId = models.AutoField(primary_key=True)
    SeqNo = models.BigIntegerField()
    BldTrnType = models.CharField(max_length=20)
    APostiveCnt = models.BigIntegerField()
    ANegativeCnt = models.BigIntegerField()
    BPositiveCnt = models.BigIntegerField()
    BNegativeCnt = models.BigIntegerField()
    ABPositiveCnt = models.BigIntegerField()
    ABNegativeCnt = models.BigIntegerField()
    OPositiveCnt = models.BigIntegerField()
    ONegativeCnt = models.BigIntegerField()
    CreatedBy = models.CharField(max_length=20)
    CreatedOn = models.CharField(max_length=20)
    class Meta:
        db_table = "tbl_BloodReports"

class LoginHistory(models.Model):
    LoginHistoryId = models.AutoField(primary_key=True)
    UserId = models.CharField(max_length=20)
    LoggedOn = models.CharField(max_length=20)
    class Meta:
        db_table = "tbl_loginHistory"

class ContactUs(models.Model):
    ContactPkId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=20)
    Email = models.CharField(max_length=20)
    ContactNo = models.BigIntegerField()
    Comments= models.CharField(max_length=250)
    Suggestion = models.CharField(max_length=250)
    PostedOn = models.CharField(max_length=20)
    isActive = models.BooleanField(default=0)
    class Meta:
        db_table = "tbl_contactUs"

class UsersImage(models.Model):
    ImageId = models.AutoField(primary_key=True)
    ImageName = models.CharField(max_length=20)
    ImageBase64String = models.TextField(max_length=20)
    ImageType = models.CharField(max_length=20)
    UpdatedOn = models.CharField(max_length=20)
    UserId = models.BigIntegerField()
    class Meta:
        db_table = "tbl_UersImage"