from pymongo import MongoClient
client = MongoClient("mongodb+srv://username:password@cluster0.dexxeof.mongodb.net/")
#replace username and pasword with your personal credentials
db = client.scrapy
collection=db.test_collection
import datetime
post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
}
posts = db.posts
post_id = posts.insert_one(post).inserted_id