class GroupsVM():
  idGroup = 0
  name = ""
  nameBook = ""
  imgPath = ""
  adress = ""
  nbParticipents = 0
  nbFreePlaces = 10
  eventDate = ""
  is_canceled = False
  is_full = False
  eventMoment = ""

  def __init__(self, name = "", nameBook = "", imgPath = "", adress = "", nbParticipents = 0, nbFreePlaces = 10, idGroup = 0, eventDate = "", is_canceled = False, is_full = False, eventMoment = ""):
    self.idGroup = idGroup
    self.name = name
    self.nameBook = nameBook
    self.imgPath = imgPath
    self.adress = adress
    self.nbParticipents = nbParticipents
    self.nbFreePlaces = nbFreePlaces
    self.eventDate = eventDate
    self.is_canceled = is_canceled
    self.is_full = is_full
    self.eventMoment = eventMoment

