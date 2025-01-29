from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Max
from django.contrib.auth.hashers import make_password
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self,email,name,password=None,**extra_fields):
        if not email:
            raise ValueError("The email field must be set")
        email=self.normalize_email(email)
        user=self.model(email=email,name=name,**extra_fields)
        # is_active = True
        if password:
            try:
                validate_password(password,user)
            except ValidationError as e:
                raise ValueError(f"Password Validation error: {e.messages}")
            user.set_password(password)
        else:
            raise ValueError("Password is required")
        
        user.save(using=self._db)
        return user
    def create_superuser(self,email,name,password=None,**extra_fields):
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email,name,password, **extra_fields)
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    name=models.CharField(max_length=200)
    email=models.EmailField(unique=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
   

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def has_perm(self, perm, obj=None): 
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def __str__(self):
        return self.email

class Department(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class Student(CustomUser):
    std_id=models.CharField(unique=True,max_length=50)
    img=models.FileField(upload_to='media/student_image',null=True)
    options=( 
        ("Male","Male"),
        ("Female","Female"),
        ("Others","Others")
    )
    gender=models.CharField(max_length=100,choices=options,default="Male")
    dob=models.DateField(null=True)
    sem = models.CharField(max_length=100,null=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        if not self.std_id:  
            last_std_id = Student.objects.aggregate(max_id=Max('std_id'))['max_id']
            if last_std_id:
                new_id = int(last_std_id[3:]) + 1
            else:
                new_id = 1
            self.std_id = f"SNC{new_id:04d}"  
            
            self.set_password('SNGCE@123')
        # if self.pk is None or not self.password:
        #     self.password = set_password('SNGCE@123')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.std_id 
    

class Event(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    cat = models.CharField(max_length=300)
    date = models.DateField()
    time = models.CharField(max_length=200)
    img = models.FileField(upload_to="media/Event_Image")
    venue = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.title
    

class Notification(models.Model):
    title = models.CharField(max_length=200)
    options = (
        ("Emergency","Emergency"),
        ("Important","Important"),
        ("General","General")
    )
    imp = models.CharField(max_length=100,choices=options)
    message = models.TextField()
    end_date = models.CharField(max_length=100,null=True)
    btn_name = models.CharField(max_length=100,null=True,blank=True)
    btn_link = models.URLField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.title
