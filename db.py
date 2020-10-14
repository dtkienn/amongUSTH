import pymongo

client = pymongo.MongoClient("mongodb+srv://Sm00thiee:123@cluster0.3ihx5.mongodb.net/?retryWrites=true&w=majority")
db = client['mydatabase']
col1 = db["student"]
col2 = db["book"]
col3 = db['discussion']

class user:
    def login(name, email):
        myquerry={"email":email}
        mydoc = col1.find_one(myquerry)
            
        if mydoc == None:
            mylist={"name":name,"email":email}
            col1.insert_one(mylist)
            print("Created!")
        else:
            print("WELCOME BACK")
    
    def get_info(email):
        querry = {'email' : email}
        doc = col1.find_one(querry)
        print(doc)

class book:
    def add(bname, bauthor, link):
        querry = {"name":bname, "link":link}
        doc = col2.find_one(querry)

        if col2.find_one(querry) == None:
            mylist = {"name":bname, "author":bauthor}
            col2.insert_one(mylist)
            print("Created book!")

        else:
            print("Book existed!")

class discussion:
    def add (title, content, author):
        querry = {'title' : title, 'content' : content}
        doc = col3.find_one(querry)

        if col2.find_one(querry) == None:
            mylist = {"title" : title, 'content' : content, "author" : author}
            col2.insert_one(mylist)
            print("Created book!")

        else:
            print("Book existed!")


    