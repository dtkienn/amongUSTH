import pymongo

client = pymongo.MongoClient("mongodb+srv://Sm00thiee:123@cluster0.3ihx5.mongodb.net/?retryWrites=true&w=majority")
db = client['mydatabase']
col = db["student"]

class user:
    def login(name, email):
        myquerry={"email":email}
        mydoc = col.find_one(myquerry)
            
        if mydoc == None:
            mylist={"name":name,"email":email}
            col.insert_one(mylist)
            print("Created!")
        else:
            print("WELCOME BACK")
    
    def get_info(email):
        querry = {'email' : email}
        doc = col.find_one(querry)
        print(doc)
