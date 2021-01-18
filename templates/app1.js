//import express for routing 
const express = require('express');//
//import body parson module wanna be use the
//parse JSON between the client side and the
//server side
const bodyParser = require("body-parser");
//create an instance of Express application

//import path module for serving a static
//HTML file to the user
//gonna tell express to use the body parson 
//and gonna parsing JSON data sent form the
//client side to the server using body path 
//module 

//import path module 
const path = require('path');
//bring database stuff 
const app = express();
app.use(bodyParser.json());
app.use('/',express.static(path.join(__dirname,'static')))
// const db = require("./dbjs");
// const collection = "User_info";
// app.get('/',(req,res) => {
// 	res.sendFile(path.join(__dirname,'profile.html'));
// });
app.post('/api/register',async (req,res)=>{
	console.log(req.body)
	res.json({status: 'ok'})
})
// const ty = db.listDatabases();
// console.log(ty);
// listDatabases(db.client);

// async function listDatabases(client){
// 	databasesList = await db.client.db().admin().listDatabases();
// 	console.log("Database:");
// 	databasesList.databases.forEach(db => console.log(`- ${db.name}`));
// };
// const getPrimaryKey = (_id)=>{
// 	return ObjectID(_id);
// }
// async function createListing(client, newlisting){
// 	const result = await db.client.db(db.dbname).collections(db.collection_u).insertOne(newlisting);
// 	console.log(result);
// }
// async function createMultiListing(client, newmultiListing){
// 	const result = await client.db(db.dbname).collections(db.collection_u).insertMany(newmultiListing);
// 	console.log(`${result.insertCount} new listing(s) create with following id(s): `);
// 	console.log(result.insertedIds);
// }
app.listen(9999,()=>{
	console.log('Server up at 9999')
})