from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

class Account(models.Model):
  user = models.OneToOneField(User, on_delete= models.CASCADE, related_name='account')
  firstName = models.CharField(max_length = 8, default='')
  lastName = models.CharField(max_length = 8, default = '')
  birthday = models.DateField(default = date.today)
  ACCOUNT_TYPE = (
    ('lb', 'libraire'),
    ('cl', 'client'),
  )
  accountType = models.CharField(
    max_length=2,
    choices = ACCOUNT_TYPE,
    default = 'cl',
  )
  adress = models.CharField(max_length = 200, default = '')
  city = models.CharField(max_length = 50, default = '')
  zipCode = models.CharField(max_length = 5, default = '0000')
  phone_number = models.CharField(max_length=15, default='0658248398')

  def __str__(self):
    return self.user.username

class Book(models.Model):
  published_by = models.ForeignKey(User, on_delete= models.DO_NOTHING, related_name='mybook', default=None)
  title = models.CharField(max_length = 100, default = "Title Book", unique=True)
  shortDescription = models.CharField(max_length = 1000, default="Short Descpriton for the book")
  resume = models.CharField(max_length=3000, default="descprtion")
  categories = (
    ('dv','diversifié'),
    ('dr','dramatique'),
    ('su','suspense'),
    ('na','naratif'),
    ('ac','action'),
    ('sc','science'),
    ('o','others')
  )
  editor = models.CharField(max_length=20, default="Alilou Raid")
  quantity = models.IntegerField(default=1)
  price = models.DecimalField(max_digits=5, decimal_places=2, default=1)
  category = models.CharField(
    max_length=15,
    choices=categories,
    default='o'
  )
  release_date = models.DateField(default=date.today)
  is_available = models.BooleanField(default=True)
  bookImage = models.ImageField(null=True,upload_to='bookPictures',default='bookPictures/droit.jpeg')

  def __str__(self):
    return self.title

class ReadingGroup(models.Model):
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
  book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='group')
  name = models.CharField(max_length=30)
  is_full = models.BooleanField(default=False)
  is_canceled = models.BooleanField(default=False)
  img = models.ImageField(null=True,upload_to='bookPictures',default='bookPictures/droit.jpeg')
  nbMembers = models.IntegerField(default=0)
  eventDate = models.DateField(default=date.today)
  eventMoment = models.TimeField(default=datetime.now().time())
  adresse = models.CharField(default='1 rue etoile', max_length=30)
  codeZip = models.IntegerField(default=75001, max_length=10)
  city = models.CharField(default='Paris', max_length=50)

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['created_by','book', 'eventDate', 'eventMoment'], name = 'unique_ReadingGroup_contraint')
    ]

  def __str__(self):
    return self.name

# Create an instance and this entity when user is added to a reading group
class MembersGroup(models.Model):
  member = models.ForeignKey(User, on_delete=models.DO_NOTHING)
  group = models.ForeignKey(ReadingGroup, on_delete=models.DO_NOTHING)

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['member','group'], name = 'unique_member_group_combination')
    ]

# Create an instance when operation done in success status and this instance when operation status became restored
class ClientBook(models.Model):
  client = models.ForeignKey(User, on_delete= models.DO_NOTHING, related_name='cb_client')
  book = models.ForeignKey(Book, on_delete=models.DO_NOTHING ,related_name='cb_book')

class SellerBook(models.Model):
  seller = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sb_seller')
  book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, related_name='sb_book')

class Operation(models.Model):
  choices=(
    ('P','pending'),
    ('S','success'),
    ('F','fail'),
    ('C','challenged'),
    ('R','restored'),
  )
  target_book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, related_name='operations', default=0)
  seller = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='operation_seller')
  client = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='operation_client')
  nbBooks = models.IntegerField()
  period_rental = models.IntegerField(max_length=4, default=10)
  rental_start_date = models.DateTimeField(default=date.today)
  is_late = models.BooleanField(default=False)
  meetingPlace = models.CharField(max_length=200)
  amount = models.DecimalField(max_digits=5, decimal_places=2)
  status = models.CharField(
    max_length=15,
    choices=choices,
    default='P'
  )

  @property
  def get_return_date_for_book(self):
    return self.nbBooks

class ChallengedOperation(models.Model):
  challenged_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='challenge_user')
  operation = models.OneToOneField(Operation, on_delete=models.DO_NOTHING, related_name='challege_operation')