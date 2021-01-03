from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MaxValueValidator
from django.conf import settings
from django.db.models import F, Count, Value, Sum, Avg
from datetime import date, timedelta
import time

from user.manager import UserObjectManager


department_dict = [('1', 'Management'),
                   ('2', 'Development'),
                   ('3', 'Sales'),
                   ('4', 'Human Resource'),
                   ('5', 'Data Entry'),
                   ('6', 'Creative'),
                   ('7', 'Digital Marketing'),
                   ]

relation_dict = [('mother', 'Mother'),
                 ('father', 'Father'),
                 ('brother', 'Brother'),
                 ('sister', 'Sister'),
                 ('wife', 'Wife'),
                 ('son', 'Son'),
                 ('daughter', 'Daughter')]


designation_choice = [
    ('trainee', 'Trainee'),
    ('jr_developer', 'Jr. Developer'),
    ('developer', 'Developer'),
    ('sr_developer', 'Sr. Developer'),
    ('atl', 'Asst. Team Lead'),
    ('tl', 'Team Lead'),
    ('apm', 'Asst Project Manager'),
    ('pm', 'Project Manager'),
    ('fd', 'Front Desk'),
    ('hr', 'Hr Manager'),
    ('SEO', 'Chief Executive officer'),
    ('CTO', 'Chief Technical officer'),
    ('BDE', 'Business Development Executive'),
    ('seo_executive','Seo Executive'),
    ('sr_seo_executive','Sr seo executive'),
    ('jr_seo_executive', 'Jr seo executive'),
    ('web_designer', 'Web Designer'),
    ('graphic_designer', 'Graphic Designer'),
    ('BDM', 'Business Development Manager')
]

designation_colore = [
    ('trainee', 'primary'),
    ('jr_developer', 'primary'),
    ('developer', 'info'),
    ('sr_developer', 'success'),
    ('atl', 'warning'),
    ('tl', 'warning'),
    ('apm', 'danger'),
    ('pm', 'danger'),
    ('fd', 'info'),
    ('BDE', 'info'),
    ('SEO', 'default'),
    ('CTO', 'default'),
]


def format_timedelta(td):
    try:
        hours, remainder = divmod(td.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        hours, minutes, seconds = int(hours), int(minutes), int(seconds)
        if hours < 10:
            hours = '0%s' % int(hours)
        if minutes < 10:
            minutes = '0%s' % minutes
        if seconds < 10:
            seconds = '0%s' % seconds
        return '%s:%s:%s' % (hours, minutes, seconds)
    except:
        return '%s:%s:%s' % (0, 0, 0)


class CustomUserManager(BaseUserManager):
    """ Well.. using BaseUserManager """

    def create_user(self, email, password):
        if not email:
            raise ValueError("Users must register an email")

        user = self.model(email=CustomUserManager.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_active = True
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def all(self, *args, **kwargs):
        return self.get_queryset().filter(is_active=True, *args, **kwargs)

    def filter(self, *args, **kwargs):
        return self.get_queryset().filter(is_active=True, *args, **kwargs)

    def employee(self, *args, **kwargs):
        return self.get_queryset().filter(*args, **kwargs)

class Skill(models.Model):
    name = models.CharField(max_length=140)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="skill_created_by", verbose_name="Created By")
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="skill_modified_by", verbose_name="Modified By")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin, UserObjectManager):
    """ Using email instead of username """
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    personal_email = models.EmailField(max_length=255, db_index=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=140, blank=True, null=True)
    last_name = models.CharField(max_length=140, blank=True, null=True)
    gender = models.CharField(max_length=255,choices=(('m', "Male"),("f","Female")), blank=True, null=True)
    phone_number = models.CharField(max_length=140, blank=True, null=True)
    alternate_phone_number = models.CharField(
        max_length=140, blank=True, null=True)
    address = models.CharField(max_length=140, blank=True, null=True)
    city = models.CharField(max_length=140, blank=True, null=True)
    state = models.CharField(max_length=140, default='')
    pin_code = models.CharField(max_length=140, blank=True, null=True)
    department = models.CharField(max_length=10, choices=department_dict)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='childs')
    skype = models.CharField(max_length=30, null=True)
    skills = models.ManyToManyField(Skill)
    date_of_joining = models.DateField(null=True, blank=True)
    employee_id = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to='', null=True, default=None, blank=True)
    machine_id = models.IntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    # date_of_next_increment = models.DateField(null=True, blank=True)
    bond_till = models.DateField(null=True, blank=True)

    notice_period = models.CharField(max_length=250, null=True, blank=True)
    designation = models.CharField(
        max_length=100, choices=designation_choice, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name

    @property
    def full_name(self):
        if (self.first_name or self.last_name):
            full_name = '%s %s' % (self.first_name, self.last_name)
            return str(full_name.strip())
        else:
            return self.email
            
        

    @property
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return str(full_name.strip())

    def get_short_name(self):
        return self.full_name

    @property
    def is_supervisor(self):
        return self.childs.exists()

    # @property
    # def leave_bank(self):
    #     added = self.leave_banks.filter(type="1").count()
    #     taken = self.leave_banks.filter(type="2").count()
    #     return added - taken

    @property
    def leave_approve(self):
        leave_not_approve = self.leaves_approval.filter(supervisor_approval = 0)
        leave_count = leave_not_approve.count()
        return leave_count


    @property
    def get_avarage_ratings(self):
        return self.feedbacks.all().aggregate(Avg('rating')).values()[0]

    @property
    def get_last_rating(self):
        return self.feedbacks.filter(rating_provided=True).last()

    def rating_positive(self):
        return self.get_last_rating.positive

    def rating_negative(self):
        return self.get_last_rating.negative

    def rating_suggestion(self):
        return self.get_last_rating.suggestion
    def rating_rating(self):
        return self.get_last_rating.rating

    def waiting_feedback(self):
        return self.tl_feedbacks.filter(rating_provided=False).count()

    def display_feedback(self):
        if date.today()> date.today().replace(day=6) and date.today()< date.today().replace(day=25):
            return self.get_last_rating
        return False

    class Meta:
        ordering = ['-first_name']


class FamilyMember(models.Model):
    full_name = models.CharField(max_length=140)
    relation_with_employee = models.CharField(
        max_length=50, choices=relation_dict)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(CustomUser, related_name='family_members')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="family_member_created_by", verbose_name="Created By")
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="family_member_modified_by", verbose_name="Modified By")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)



class TlFeedback(models.Model):
    """docstring for Feedback"""
    user = models.ForeignKey(CustomUser, related_name='feedbacks')
    tl = models.ForeignKey(CustomUser, related_name='tl_feedbacks')
    created_at = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=1, choices = [(i,i) for i in range(1,11)])
    positive = models.TextField(null=True, blank=True)
    negative = models.TextField(null=True, blank=True)
    suggestion = models.TextField(null=True, blank=True)
    rating_provided = models.BooleanField(default=False)

    @classmethod
    def generate_records(cls):
        tdate = date.today()
        users = CustomUser.objects.filter(department__in=['2','5','6','7'])
        for  user in users:
            if user.parent.department != '1' and tdate > date.today().replace(day=24) and tdate < date.today().replace(day=29):
                if not cls.objects.filter(user= user, tl = user.parent, created_at__month=tdate.month, created_at__year=tdate.year):
                    cls.objects.create(user= user, tl = user.parent)
                    print ("working")
                else:
                    print("out of create , get found ")
            else:
                print ("Date is not in Range")

    @classmethod
    def delete_pending(cls):
        tdate = date.today()
        if tdate > date.today().replace(day=6):
            cls.objects.filter(rating_provided=False).delete()
