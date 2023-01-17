class LoansVM():
    target_book_id = 0
    book_title = ""
    othor_username = ""
    returned_date = ""
    delay_in_days = 0
    nbBooks = 0
    operationID = 0
    
    def __init__(self, book_title="", othor_username="", returned_date="", delay_in_days=0, nbBooks=0, operationID=0, target_book_id = 0):
        self.target_book_id = target_book_id
        self.book_title = book_title
        self.othor_username = othor_username
        self.returned_date = returned_date
        self.delay_in_days = delay_in_days
        self.nbBooks = nbBooks
        self.operationID = operationID