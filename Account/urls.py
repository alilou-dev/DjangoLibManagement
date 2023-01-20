from django.urls import path
from Account import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
  path('create/', views.createAccount, name="accountCreation"),
  path('newbook/', views.addBook, name="BookCreate"),
  path('mylibrary/',views.publishedBooks, name="MyLibrary"),
  path('library/',views.allBooks,name='Library'),
  path('mybooks/',views.rentedBooks,name='MyBooks'),
  path('requestBook/<int:bookId>',views.requestBook, name='RequestBook'),
  path('manageclientrequest/',views.manageClientRequest,name='ClientRequests'),
  path('managesellerrequest/',views.manageSellerRequest,name='SellerRequests'),
  path('challengeOperation/<int:operationId>',views.challengeClientRequest,name='NewRequest'),
  path('requestSellerDone',views.requestSellerDone, name='RequestDone'),
  path('loansSeller/',views.manageSellerLoans, name='SellerLoans'),
  path('requestClientDone/',views.requestClientDone, name='RequestDone'),
  path('acceptRequestSeller/<int:operationID>', views.acceptSellerRequest, name='AcceptRequest'),
  path('refuseRequestSeller/<int:operationID>',views.refuseSellerRequest, name='RefuseRequest'),
  path('acceptRequestClient/<int:operationID>', views.acceptClientRequest, name='AcceptRequest'),
  path('refuseRequestClient/<int:operationID>', views.refuseClientRequest, name='RefuseRequest'),
  path('restoreBook/<int:operationID>', views.markRequestAsRestored,name='RestoreRequest'),
  path('manageBook/<int:bookID>', views.managePublishedBook, name='ManageBook'),
  path('allReadingGroup', views.allReadingGroups, name='ReadingGroup'),
  path('createReadingGroup/<int:bookID>',views.createReadingGroup, name='CreateGroup'),
  path('manageReadingGroupsForClient', views.manageClientReadingGroup, name='ManageGroup'),
  path('manageReadingGroupsForSeller', views.manageSellerReadingGroup, name='ManageGroup'),
  path('removeGroup/<int:groupID>', views.cancelReadingGroup, name="RemoveGroup"),
  path('joinGroup/<int:groupID>', views.joinReadingGroup, name='JoinGroup')
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

