from cgitb import html
from django.contrib import messages
from django.shortcuts import render, redirect
from main.form import AccountCreationForm, BookCreationForm, RequestForBookForm, ManageBookForm, AddReadingGroupForm, ChallengeRequestForm
from django.contrib.auth.models import User
from Account import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from datetime import datetime, timedelta, timezone
from main.templates.registration import *
from Account.viewModels.ManageRequestVM import ManageRequestVM
from Account.viewModels.LoansVM import LoansVM
from Account.viewModels.GroupsVM import GroupsVM
from DjangoBib.decorators.noAccountHolder import no_userHasAccount_required
from DjangoBib.decorators.userMustBeSeller import perm_seller_required
from DjangoBib.decorators.userMustBeClient import perm_client_required
from django.db import IntegrityError
# Create your views here.

@no_userHasAccount_required
def createAccount(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)    
        if form.is_valid():
            accountType = request.POST['accountType']
            
            models.Account.objects.create(
                user = request.user,
                firstName = request.POST['firstName'],
                lastName = request.POST['lastName'],
                birthday = request.POST['birthday'],
                adress = request.POST['adress'],
                zipCode = request.POST['zipCode'],
                city = request.POST['city'],
                phone_number = request.POST['phone_number'],
                accountType = accountType,
            )
            ctPermHasAccount = ContentType.objects.get_for_model(models.Account)
            permissionHasAccount = Permission.objects.get(
                codename='change_account',
                content_type=ctPermHasAccount,
            )
            request.user.user_permissions.add(permissionHasAccount)
            
            if(accountType == 'lb'):
                ctPermAddBook = ContentType.objects.get_for_model(models.Book)
                permissionAddBook = Permission.objects.get(
                    codename='add_book',
                    content_type=ctPermAddBook,
                )
                request.user.user_permissions.add(permissionAddBook)
                
            return redirect("/home")
    else : 
        form = AccountCreationForm()        
    return render(request, 'accountCreate.html' ,{'form': form})

@perm_seller_required        
def addBook(request):
    if request.method == 'POST':
        form = BookCreationForm(request.POST)
        if form.is_valid():
            
            #first create the book
            newBook = models.Book.objects.create(
                published_by = request.user,
                title = request.POST['title'],
                editor = request.POST['editor'],
                shortDescription = request.POST['shortDescription'],
                resume = request.POST['resume'],
                category = request.POST['category'],
                quantity = request.POST['quantity'],
                price = request.POST['price'],
                release_date = request.POST['release_date'],
                bookImage = request.POST['img'],
            )
            
            #second create instance of sellerBook
            addRelationBookSeller(newBook, request.user)
            
            return redirect("/account/mylibrary")
    else :
        form = BookCreationForm()
    return render(request, 'bookCreate.html', {'form' : form})                    
    
@perm_seller_required    
def publishedBooks(request):
    bookIds = models.SellerBook.objects.filter(seller = request.user).values('book_id')
    books = list()
    for id in bookIds : 
        result = models.Book.objects.filter(pk = id['book_id']).values()[0] 
        books.append(result)
        
    return render(request, 'sellerLibrary.html', {'books' : books})    


@perm_client_required
def allBooks(request):
    allBooks = models.Book.objects.all().values()
    return render(request,'clientLibrary.html', {'books' : allBooks})

@perm_client_required
def rentedBooks(request):
    operations_done = models.Operation.objects.filter(client = request.user).filter(status = 'S')
    loans = list(operations_done.values())
    loansVM = []
    #build view model for client loans
    for op in loans :
        delay_in_days = 0 
        book_title = models.Book.objects.filter(pk = op["target_book_id"]).values('title')[0]['title']
        client_username = models.User.objects.filter(pk = op['seller_id']).values('username')[0]['username']
        returned_date = op['rental_start_date'] + timedelta(days= op['period_rental']) 
        dt = datetime.now().replace(tzinfo=timezone.utc)    
        diff = (returned_date - dt + timedelta(days=1)).days
        if diff < 0 : 
            delay_in_days = diff
            vm = LoansVM(book_title, client_username, returned_date, abs(delay_in_days))
        else : 
            vm = LoansVM(book_title, client_username, returned_date)    
        loansVM.append(vm)
    return render(request, 'clientRentedBook.html', {'loans' : loansVM})

@perm_client_required
def requestBook(request, bookId):
    if request.method == 'POST':
        form = RequestForBookForm(request.POST)
        if form.is_valid():
            if int(request.POST['quantity']) < models.Book.objects.filter(pk = bookId).values('quantity')[0]['quantity']: 
                seller = models.SellerBook.objects.filter(book_id = bookId).values('seller_id')[0]['seller_id']
                #create the operation first
                result = models.Operation.objects.create(
                    target_book = models.Book.objects.get(pk = bookId),
                    seller_id = seller,
                    client = request.user,
                    amount = request.POST['amount'],
                    meetingPlace = request.POST['adress'],
                    nbBooks = request.POST['quantity'],
                    period_rental = request.POST['period_rental'],
                )
            else :
                # maybe add message to say that there is not inoff quantity of book to do the request
                return redirect('/account/library') 
            return redirect("/account/manageclientrequest")
    else :
        form = RequestForBookForm()    
    return render(request, 'requestBook.html', {'form': form})

@perm_client_required
def manageClientRequest(request):
    
    result = models.Operation.objects.filter(client = request.user).filter(status = 'P') | models.Operation.objects.filter(client = request.user).filter(status = 'C')
    requests = list(result.values())
    requestsVM = []
    
    #build view model
    for req in requests :
        challengedByMe = False
        result = models.ChallengedOperation.objects.filter(operation_id = req['id']).values('challenged_by_id')
        if result.exists() :
            # get the user whose is the last challenger
            last_user_challenged = models.User.objects.get(pk = result[0]['challenged_by_id'])
            if last_user_challenged == request.user :
                challengedByMe = True
                
        othor = models.User.objects.filter(pk = req['seller_id']).values('username')[0]['username']
        amount = req['amount']
        status = req['status']
        nbBooks = req['nbBooks']
        nbDays = req['period_rental']
        book_title = models.Book.objects.filter(pk = req["target_book_id"]).values('title')[0]['title']
        operationID = req['id']
        book_id = req['target_book_id']
        vm = ManageRequestVM(status,othor,amount,nbBooks,nbDays,book_title,operationID,book_id,challengedByMe)
        requestsVM.append(vm)
    return render(request, 'manageClientRequest.html', {'requests': requestsVM})

@perm_seller_required   
def manageSellerRequest(request):
    #test for operations thsose have status success or fail for ex
    result = models.Operation.objects.filter(seller = request.user).filter(status = 'P') | models.Operation.objects.filter(seller = request.user).filter(status = 'C')
    requests = list(result.values())
    requestsVM = []
    
    #build view model
    for req in requests :
        # check if it's actually challenged by the current user
        challengedByMe = False
        result = models.ChallengedOperation.objects.filter(operation_id = req['id']).values('challenged_by_id')
        if result.exists() :
            # get the user whose is the last challenger
            last_user_challenged = models.User.objects.get(pk = result[0]['challenged_by_id'])
            if last_user_challenged == request.user :
                challengedByMe = True
                
        othor = models.User.objects.filter(pk = req['client_id']).values('username')[0]['username']
        amount = req['amount']
        status = req['status']
        nbBooks = req['nbBooks']
        nbDays = req['period_rental']
        book_title = models.Book.objects.filter(pk = req["target_book_id"]).values('title')[0]['title']
        book_id = req['target_book_id']
        operationID = req['id']
        vm = ManageRequestVM(status,othor,amount,nbBooks,nbDays,book_title,operationID,book_id,challengedByMe)
        requestsVM.append(vm)
        
    return render(request, 'manageSellerRequest.html', {'requests': requestsVM})

def challengeClientRequest(request, operationId):
    if request.method == 'POST':
        form = ChallengeRequestForm(request.POST)
        if form.is_valid():
            result = models.Operation.objects.filter(pk = operationId).update(meetingPlace = request.POST['adress'], nbBooks = request.POST['quantity'], period_rental = request.POST['period_rental'], amount = request.POST['amount'], status = 'C')
            if(result == 1):
                #CREATE A CHALLENGEDOPERATION
                try :
                   models.ChallengedOperation.objects.filter(operation_id = operationId).update(challenged_by = request.user)
                except models.ChallengedOperation.DoesNotExist : 
                       models.ChallengedOperation.objects.create(
                           challenged_by = request.user,
                           operation_id = operationId,
                       ) 
                return redirect("/account/managesellerrequest")
            else :
                return redirect('home')    
            
    else :
          form = RequestForBookForm()       
    return render(request,'challengeOperation.html', {'form' : form})
    
@perm_seller_required    
def requestSellerDone(request):
    #returner toute les opération achevées or sois fails sois restored
    operations_done = models.Operation.objects.filter(seller = request.user).filter(status = 'R') | models.Operation.objects.filter(seller = request.user).filter(status = 'F')
    requests = list(operations_done.values())
    requestsVM = []
     #build view model
    for req in requests :
        othor = models.User.objects.filter(pk = req['client_id']).values('username')[0]['username']
        amount = req['amount']
        status = req['status']
        nbBooks = req['nbBooks']
        nbDays = req['period_rental']
        book_title = models.Book.objects.filter(pk = req["target_book_id"]).values('title')[0]['title']
        operationID = req['id']
        vm = ManageRequestVM(status,othor,amount,nbBooks,nbDays,book_title,operationID)
        requestsVM.append(vm)
        
    return render(request, 'requestSellerDone.html', {'requests': requestsVM})

@perm_seller_required
def manageSellerLoans(request):
    #return only operations those have status 'S' or operations that is have been rented (S to success)
    operations_done = models.Operation.objects.filter(seller = request.user).filter(status = 'S')
    loans = list(operations_done.values())
    loansVM = []
    #build view model for seller loans
    for op in loans : 
        delay_in_days = 0
        book_title = models.Book.objects.filter(pk = op["target_book_id"]).values('title')[0]['title']
        client_username = models.User.objects.filter(pk = op['client_id']).values('username')[0]['username']
        nbBooks = op['nbBooks']
        returned_date = op['rental_start_date'] + timedelta(days= op['period_rental']) 
        dt = datetime.now().replace(tzinfo=timezone.utc)    
        diff = (returned_date - dt + timedelta(days=1)).days
        if diff < 0 : 
            delay_in_days = diff
            vm = LoansVM(book_title, client_username, returned_date, abs(delay_in_days), nbBooks, operationID=op['id'])
        else : 
            vm = LoansVM(book_title, client_username, returned_date,nbBooks=nbBooks, operationID=op['id'])    
        loansVM.append(vm)
    return render(request, 'loansSeller.html', {'loans' : loansVM})

@perm_client_required
def requestClientDone(request):
    #returner toute les opération achevées or fails
    operations_done = models.Operation.objects.filter(client = request.user).filter(status = 'R') | models.Operation.objects.filter(client = request.user).filter(status = 'F')
    requests = list(operations_done.values())
    requestsVM = []
     #build view model
    for req in requests :
        othor = models.User.objects.filter(pk = req['seller_id']).values('username')[0]['username']
        amount = req['amount']
        status = req['status']
        nbBooks = req['nbBooks']
        nbDays = req['period_rental']
        book_title = models.Book.objects.filter(pk = req["target_book_id"]).values('title')[0]['title']
        operationID = req['id']
        vm = ManageRequestVM(status,othor,amount,nbBooks,nbDays,book_title,operationID)
        requestsVM.append(vm)
        
    return render(request, 'requestClientDone.html', {'requests': requestsVM})

@perm_seller_required
def acceptClientRequest(request, operationID):
    nbBookRequested = models.Operation.objects.filter(pk = operationID).values('nbBooks')[0]['nbBooks']
    #update quantity for the requested book 
    target_book_id = models.Operation.objects.filter(pk = operationID).values('target_book_id')[0]['target_book_id']
    #update the target book
    actuelQuantity = models.Book.objects.filter(pk = target_book_id).values('quantity')[0]['quantity']
    models.Book.objects.filter(pk = target_book_id).update(quantity = actuelQuantity - nbBookRequested)
    models.Operation.objects.filter(pk = operationID).update(status = 'S', rental_start_date = datetime.now().strftime('%Y-%m-%d %H:%M'))
    # get the id of the client whose requested for the book 
    client_id = models.Operation.objects.filter(pk = operationID).values('client_id')[0]['client_id']
    models.ClientBook.objects.create(
        client_id = client_id, 
        book_id = target_book_id,
    )
    return redirect('/account/loansSeller')

@perm_client_required
def acceptSellerRequest(request, operationID):
    nbBookRequested = models.Operation.objects.filter(pk = operationID).values('nbBooks')[0]['nbBooks']
    #update quantity for the requested book 
    target_book_id = models.Operation.objects.filter(pk = operationID).values('target_book_id')[0]['target_book_id']
    #update the target book
    actuelQuantity = models.Book.objects.filter(pk = target_book_id).values('quantity')[0]['quantity']
    models.Book.objects.filter(pk = target_book_id).update(quantity = actuelQuantity - nbBookRequested)
    models.Operation.objects.filter(pk = operationID).update(status = 'S', rental_start_date = datetime.now().strftime('%Y-%m-%d %H:%M'))
    # get the id of the client whose requested for the book 
    client_id = models.Operation.objects.filter(pk = operationID).values('client_id')[0]['client_id']
    models.ClientBook.objects.create(
        client_id = client_id, 
        book_id = target_book_id,
    )
    return redirect('/account/mybooks')

@perm_client_required
def refuseSellerRequest(request, operationID):  
    models.Operation.objects.filter(pk = operationID).update(status = 'F')
    return redirect('/account/manageclientrequest')

@perm_seller_required
def refuseClientRequest(request, operationID):
    models.Operation.objects.filter(pk = operationID).update(status = 'F')
    return redirect('/account/managesellerrequest')

@perm_seller_required
def markRequestAsRestored(request, operationID):
    # mark the resquest as restored with updating the status 
    models.Operation.objects.filter(pk = operationID).update(status = 'R')
    # first get the nbBooks that have been rented from the operation and after get the id of the target book
    nbBooks = models.Operation.objects.filter(pk = operationID).values('nbBooks')[0]['nbBooks']
    target_book_id = models.Operation.objects.filter(pk = operationID).values('target_book_id')[0]['target_book_id']
    actuelQuantityBooks = models.Book.objects.filter(pk = target_book_id).values('quantity')[0]['quantity']
    # update quantity
    newQuantity = actuelQuantityBooks + nbBooks
    models.Book.objects.filter(pk = target_book_id).update(quantity = newQuantity)
    return redirect('/account/requestSellerDone')

@perm_seller_required
def managePublishedBook(request, bookID):
    # here we have the id of the book to manage (change the quantity for exemple), TODO : add away to manage properly the seller books
    book = models.Book.objects.get(pk = bookID)
    if request.method == 'POST':
        form = ManageBookForm(request.POST)
        if form.is_valid():
            # TODO : update the book requested after checking what field must be updated (check if request.POST['name_field'] !== "")
            newTitle = request.POST['newTitle']
            newEditor = request.POST['newEditor']
            newQuantity = request.POST['newQuantity']
            newPrice = request.POST['newPrice']
            newCategory = request.POST['newCategory']
            newImg = request.POST['newImg']
            
            if newTitle != "":
                setattr(book, 'title', newTitle)
            if newEditor != "":
                setattr(book,'editor', newEditor)
            if newQuantity != "":
                setattr(book, 'quantity', newQuantity)
            if newPrice != "":
                setattr(book, 'price', newPrice)
            if newCategory != "":
                setattr(book, 'category', newCategory)
            if newImg != "":
                setattr(book, 'bookImage', newImg)    
                
            book.save()
            # update the book 
            return redirect('/account/mylibrary')
    else :
        form = ManageBookForm()
        
    return render(request, 'managePublishedBook.html', {'form': form})

@perm_client_required
def allReadingGroups(request):
    # get all reading groupe that have been created
    allReadingGroup = models.ReadingGroup.objects.filter(is_canceled = False)
    groups = list(allReadingGroup.values())
    groupsVM = []
    for group in groups : 
        id = group['id']
        name = group['name']
        nameBook = models.Book.objects.filter(pk = group['book_id']).values('title')[0]['title']
        imgPath = group['img']
        adress = group['adresse'] + ', ' + group['city'] + ', ' + str(group['codeZip'])
        nbParticipents = group['nbMembers']
        is_full = group['is_full'] 
        nbFreePlaces = 10 - nbParticipents
        is_canceled = group['is_canceled']
        eventDate = group['eventDate']
        eventMoment = group['eventMoment']
        vm = GroupsVM(idGroup= id, nameBook = nameBook, name = name, imgPath=imgPath, adress = adress, nbParticipents= nbParticipents, is_full = is_full, is_canceled= is_canceled, nbFreePlaces= nbFreePlaces, eventDate= eventDate, eventMoment= eventMoment)
        groupsVM.append(vm)
    return render(request, 'allGroupsForClient.html', {'groups': groupsVM})

@perm_seller_required
def createReadingGroup(request, bookID):
    if request.method == 'POST':
        form = AddReadingGroupForm(request.POST)
        if form.is_valid():
            #first create the group
            newBook = models.ReadingGroup.objects.create(
                created_by = request.user,
                book_id = bookID,
                name = request.POST['name'],
                img = request.POST['img'],
                eventDate = request.POST['eventDate'],
                eventMoment = request.POST['eventMoment'],
                adresse = request.POST['adress'],
                codeZip = request.POST['zipCode'],
                city = request.POST['city'],
            )
            return redirect("/account/manageReadingGroupsForSeller")
    else :
        form = AddReadingGroupForm()
            
    return render(request, 'createReadingGroup.html', {'form' : form}) 

@perm_client_required
def manageClientReadingGroup(request):
    groupsCurrentClient = models.MembersGroup.objects.filter(member = request.user).values('group')
    return render(request, 'manageClientGroups.html', {'groups' : groupsCurrentClient})

@perm_seller_required
def manageSellerReadingGroup(request):
    #retreive all groups that's have been created by the current seller
    groupsCurrentSeller = models.ReadingGroup.objects.filter(created_by = request.user)
    groups = list(groupsCurrentSeller.values())
    groupsVM = []
    #build view model for client loans
    for group in groups :
        id = group['id']
        name = group['name']
        nameBook = models.Book.objects.filter(pk = group['book_id']).values('title')[0]['title']
        imgPath = group['img']
        adress = group['adresse'] + ', ' + group['city'] + ', ' + str(group['codeZip'])
        nbParticipents = group['nbMembers']
        is_full = group['is_full'] 
        nbFreePlaces = 10 - nbParticipents
        is_canceled = group['is_canceled']
        eventDate = group['eventDate']
        eventMoment = group['eventMoment']
        
        vm = GroupsVM(name = name, nameBook= nameBook, imgPath=imgPath, adress = adress, nbParticipents = nbParticipents, nbFreePlaces = nbFreePlaces, idGroup= id, is_canceled = is_canceled, eventDate = eventDate, is_full = is_full)
        groupsVM.append(vm)
        
    return render(request, 'manageSellerGroups.html', {'groups' : groupsVM})

@perm_seller_required
def cancelReadingGroup(request, groupID):
    groupToCancel = models.ReadingGroup.objects.get(pk = groupID)
    groupToCancel.is_canceled = True
    groupToCancel.save()
    return redirect('/account/manageReadingGroupsForSeller')

# TODO call the private method addRelationGroupMember when user joins a group
@perm_client_required
def joinReadingGroup(request, groupID):
    group = models.ReadingGroup.objects.get(pk = groupID)
    if group.is_full : 
        # TODO message error the groups is complete (block the user on front to dont let him ask for group those are full with is_full attribute on ReadingGroup)
        return redirect('/account/manageReadingGroupsForClient')
    else :
        # first check if client has rented the book
        if isBookInUserLoans(request.user,group.book) :
            # TODO add error message to say the user has no rented the book to be able to join this group 
            
            return redirect('/account/allReadingGroup')
        # add the client in the group
        addRelationMemberGroup(group, request.user)
        # set if it's appropriate the availability group (full or not)
        checkAndSetOrNotAvailabilityGroup(group)
        return redirect('/account/manageReadingGroupsForClient')

@perm_client_required
def leaveReadingGroup(request, groupID):
    
    return redirect('/account/manageReadingGroupsForClient')


# private methods
def addRelationBookSeller(book,user):
    models.SellerBook.objects.create(
        seller = user,
        book = book,
    )
    
def addRelationMemberGroup(group, user):
    # add the user first
    try : 
        result = models.MembersGroup.objects.create(
            member = user,
            group = group,
        )
    except IntegrityError :
        # TODO add message error user already memeber of group
        return redirect('/account/manageReadingGroupsForClient')    
        
    # then increment number of members
    newNb = group.nbMembers + 1
    setattr(group, 'nbMembers', newNb)
    group.save()

# Private method for joinGroup (request from Client)        
def checkAndSetOrNotAvailabilityGroup(group):
    if group.nbMembers > 9 : 
        setattr(group, 'is_full', True)
        group.save()
# Sumury : check if the user can join the group after checking his loans (if the target_book is in his loans on not)
def isBookInUserLoans(user, book):
    result = False
    getLoanBookIfExists = models.Operation.objects.filter(client = user, target_book = book)
    if getLoanBookIfExists.count() > 0 : 
        result = True
    return result
        
    
# faire les emprunts coté seller (DONE)
# d'abord testé le retard coté client ensuite gérer le retard coté seller (DONE)
# la gestion des book coté seller (DONE)
# recherche par zone géographique et username (TODO)
# créer des groupe de lecture et les conditions pour pouvoir s'ajouter au groupe (INPROGRESS)
# create private function checkIfUserRentedTheTargetBookOfTheReadingBook for JoinGroups (TODO)
# improve challengeRequestClient so that we can challenge ONLY one or many things of the requestClient gérer le vocabulaire dans challengeOperation.html see(TODO)   
# problème avec les images     
    