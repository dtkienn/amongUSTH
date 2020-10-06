import pymongo

client = pymongo.MongoClient("mongodb+srv://Sm00thiee:123@cluster0.3ihx5.mongodb.net/?retryWrites=true&w=majority")
db = client['mydatabase']
col = db["student"]

class user:
    def login(a,b,c,d):
        myquerry={"email":c}
        mydoc = col.find_one(myquerry)
            
        if mydoc == None:
            mylist={"uid":a,"name":b,"email":c, "password" : d}
            col.insert_one(mylist)
        else:
            print("WELCOME BACK")
    
    def get_info(email):
        querry = {'email' : email}
        doc = col.find_one(querry)
        print(doc)
