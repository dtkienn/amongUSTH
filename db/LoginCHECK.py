import pymongo
client = pymongo.MongoClient("mongodb+srv://Quangg:2451@cluster0.3ihx5.mongodb.net/?retryWrites=true&w=majority")
db = client["mydatabase"]
col=db["students"]

def loginCheck(a,b,c):
    myquerry={"email":c}
    mydoc = col.find_one(myquerry)
        
    if mydoc == None:
        mylist={"name":a,"id":b,"email":c}
        col.insert_one(mylist)
    else:
        print("WELCOME BACK")


#testing DATA 
name = "QUANG"
idd = "BI9-194"
email = "aaaaaa.bi9194@st.usth.edu.vn"

loginCheck(name,idd,email)