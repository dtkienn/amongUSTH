import pymongo

client = pymongo.MongoClient("mongodb+srv://Sm00thiee:123@cluster0.3ihx5.mongodb.net/?retryWrites=true&w=majority")
db = client['mydatabase']
users = db["student"]
book = db["book"]
diss = db['discussion']
cmt = db['comment']

class user:
    def login(name, email):
        query={"email":email}
        doc = users.find_one(query)
            
        if doc == None:
            mlist={"name":name,"email":email}
            users.insert_one(mlist)
            print("Created!")
        else:
            print("WELCOME BACK")
    
    def get_info(email):
        query = {'id' : email}
        doc = users.find_one(query)
        print(doc)

class book:
    def add(bname, bauthor, link):
        query = {"name":bname, "link":link}
        doc = book.find_one(query)

        if book.find_one(query) == None:
            mylist = {"name":bname, "author":bauthor}
            book.insert_one(mylist)
            print("Created book!")

        else:
            print("Book existed!")

class discussion:
    def add (title, content, author):
        query = {'content' : content}
        doc = diss.find_one(query)

        if diss.find_one(query) == None:
            mylist = {'_id' : "0",  "title" : title, 'content' : content, "author" : author}
            diss.insert_one(mylist)
            print("Created discussion!")

        else:
            print("Content existed!")

    def comment(uid, content):
        query = {''}
    