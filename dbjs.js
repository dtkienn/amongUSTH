const {MongoClient} = require('mongodb');
const ObjectID = require('mongodb').ObjectID;
const dbname = "User";
const collection_u = "Student";
const uri = "mongodb://Sm00thiee:123@cluster0-shard-00-02.3ihx5.mongodb.net:27017,cluster0-shard-00-00.3ihx5.mongodb.net:27017,cluster0-shard-00-01.3ihx5.mongodb.net:27017/admin?ssl=true&replicaSet=atlas-hqbh5p-shard-0&readPreference=primary&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1&3t.uriVersion=3&3t.connection.name=atlas-hqbh5p-shard-0&3t.databases=admin&3t.alwaysShowAuthDB=true&3t.alwaysShowDBFromUserRole=true&3t.sslTlsVersion=TLS";
const client = new MongoClient(uri);
// async function main(){
// 	try{
// 		await client.connect();
// 		// await listDatabases(client);
// 	}catch(e){
// 		console.error(e);
// 	}finally{
// 		await client.close();
// 	}
// }
// main().catch(console.error);


// async function listDatabases(client){
// 	databasesList = await client.db().admin().listDatabases();
// 	console.log("Database:");
// 	databasesList.databases.forEach(db => console.log(`- ${db.name}`));
// };
const getPrimaryKey = (_id)=>{
	return ObjectID(_id);
}
// async function createListing(client, newlisting){
// 	const result = await client.db(dbname).collections(collection_u).insertOne(newlisting);
// 	console.log(result);
// }
// async function createMultiListing(client, newmultiListing){
// 	const result = await client.db(dbname).collections(collection_u).insertMany(newmultiListing);
// 	console.log(`${result.insertCount} new listing(s) create with following id(s): `);
// 	console.log(result.insertedIds);
// }
module.exports = {getPrimaryKey,client,dbname,collection_u}; 