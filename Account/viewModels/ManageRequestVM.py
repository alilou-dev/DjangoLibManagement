# Keep there models for your views needs
class ManageRequestVM():
  status = ""
  othor = ""
  amount = 0
  nbBooks = 0
  nbDays = 0
  book_title = ""
  operationID = 0
  book_id = 0
  challengedByMe = False

  def __init__(self, status="",othor="",amount=0, nbBooks = 0, nbDays = 0, book_title="",operationID = 0, book_id = 0, challengedByMe = False):
    if(status == 'P'):
      status = 'En Attente'
      self.status = status
    if(status == 'S'):
      status = 'Accepté'
      self.status = status
    if(status == 'F'):
      status = 'Refuser'
      self.status = status
    if(status == 'C'):
      status = 'Challengé'
    if(status == 'R'):
      status = 'Remis par le Client'

    self.status = status
    self.othor = othor
    self.amount = amount
    self.nbBooks = nbBooks
    self.nbDays = nbDays
    self.book_title = book_title
    self.operationID = operationID
    self.book_id = book_id
    self.challengedByMe = challengedByMe




