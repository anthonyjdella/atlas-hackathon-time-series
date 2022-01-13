from pymongo import MongoClient

client = pymongo.MongoClient('mongodb+srv://dbUserAnthony:oAbAcJHGCh3qlf7x@cluster0.9ptvo.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.test