// MongoDB Compass queries
// Find all documents in the collection
//db.getCollection('collection').find( <query>, <projection>, <options> )
//
// podman exec -it auth bash
// mongosh -u chris -p maGazine1!
//
db.getCollection('collection').find({})
// show dbs
// use registerdb
//
//  show collections, tables
// show collections
//
// show all documents on User collection
// db.collection.find( <query>, <projection>, <options> )
db.users.find()
//
// delete collection Users
// take care of case sensitivity
db.users.drop()
db.User.drop()
// delete database
db.dropDatabase()
//
// projection
// db.collection.find({}, {field1: 1, field2: 1})
// db.collection.find({}, {field1: 0, field2: 0})
db.users.find({}, {email: 1, username: 1})
//
// query
// Equality Condition
// {email: "chris@ibm.com"}
db.users.find({email: "chris@ibm.com"})
//
db.users.find({created_at: {$gte: ISODate('2025-02-20')}}, {email: 1, created_at: 1})
//
db.users.find({created_at: {$gte: ISODate('2025-02-20'), $lt: ISODate('2025-03-01')}}, {email: 1, created_at: 1})
//
// And
db.users.find({$and: [{disabled: false, email: "chris@ibm.com"}]})