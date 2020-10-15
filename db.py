import pymongo

client = pymongo.MongoClient("mongodb+srv://Sm00thiee:123@cluster0.3ihx5.mongodb.net/?retryWrites=true&w=majority")
db = client['mydatabase']
users = db["student"]
book = db["book"]
diss = db['discussion']
cmt = db['comment']

db.orgid_counter.insert({'_id': "userid", 'seq': 0})  
def getNextSequence(collection,name):  
   return collection.find_and_modify(query= { '_id': name },update= { '$inc': {'seq': 1}}, new=True ).get('seq');  
db.users.insert({'_uid': getNextSequence(db.orgid_counter,"userid"), 'name': "Sara a"})  

class user:
    def login(name, email):
        myquerry={"email":email}
        mydoc = users.find_one(myquerry)
            
        if mydoc == None:
            mylist={"name":name,"email":email}
            users.insert_one(mylist)
            print("Created!")
        else:
            print("WELCOME BACK")
    
    def get_info(email):
        querry = {'id' : email}
        doc = users.find_one(querry)
        print(doc)

class book:
    def add(bname, bauthor, link):
        querry = {"name":bname, "link":link}
        doc = book.find_one(querry)

        if book.find_one(querry) == None:
            mylist = {"name":bname, "author":bauthor}
            book.insert_one(mylist)
            print("Created book!")

        else:
            print("Book existed!")

class discussion:
    def add (title, content, author):
        querry = {'content' : content}
        doc = diss.find_one(querry)

        if diss.find_one(querry) == None:
            mylist = {'_id' : "0",  "title" : title, 'content' : content, "author" : author}
            diss.insert_one(mylist)
            print("Created discussion!")

        else:
            print("Content existed!")

    def comment(uid, content):
        querry = {''}
    