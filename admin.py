from login.mongo import Book, User

class book_manage():
    def approve(id_):
        Book.set_status(id_, 'aprove')
    
    def get_pending():
        Book.get_pending()

    def refuse(id_):
        Book.set_status(id_, 'refuse')

class manage_user():
    def get_online():
        User.get_online()