# Bat Tracker

![bat-tracker](/bat.jpg)

## MongoDB Atlas Hackathon Time Series

---

💚 This is my submission for the [MongoDB Atlas Hackathon](https://dev.to/devteam/announcing-the-mongodb-atlas-hackathon-on-dev-4b6m) on DEV. The category is "Prime Time" for [Time Series Collections]( v).

---
### Disclaimer

For this project, I wanted to work with technologies that I've never used. These were Django and MongoDB.

---

### About

[Movebank](https://www.movebank.org/cms/movebank-main), is a public database, where scientists track animal movements by attaching a GPS device to the animal. Based on a certain frequencies, that data is recorded by the device and stored in the database.

There is a public API which gets this data, so developers can use it in various projects.

My idea for this was to:

1. Get European free-tailed bat tracking data from Movebank's API.
2. Store that data in MongoDB.
3. Convert it to Time Series data.
4. Display that data on a Map to track their movement history.

---

### Incomplete

Unfortunately, I saw this Hackathon only a few days before the due date and did not have enough time to complete my idea. But I am submitting it as is. I may want to complete it in the future.

What I completed:

- ✅  Get European free-trailed bat tracking data from Movebank's API
- ✅  Store that data in MongoDB.
- ⛔ Convert it to Time Series data.
- ⛔ Display that data on a Map to track their movement history.

---


### Run
`pip install -r requirements.txt` - install dependencies

`python manage.py runserver` - start the server

---

### Documentation

The data handling is in `myfirstapp/models.py`. I have included detailed comments in the code to explain what I'm doing.

Here's a summary:

1. Connect to my MongoDB client
2. Get the JSON response for my data
3. Write it to a JSON file
4. Import that file as documents in my MongoDB Collection

What I am doing is this following:
    - Authenticate by logging in with credentials to Movebank
    - Use an HTTP GET Request to get the data from Movebank's public API.
        - Within my request's query string, I am specifying that I only want to GET data for X type of animal.
    - Convert this data to CSV and JSON format, for nice compatibility with Atlas Collections.

    - Now that I have the data I want in JSON, I can import this data into a MongoDB Atlas cluster.
    - I install mongoimport, then import this data from the command line.

---

### Resources

- To install MongoDB Shell and login: https://docs.mongodb.com/mongodb-shell/

```
mongosh mongodb+srv://USER:PASS@cluster0.9ptvo.mongodb.net/Bat_DB?retryWrites=true&w=majority
```

- To install MongoDB Community Edition 5.0: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/#install-mongodb-community-edition

```
brew tap mongodb/brew
brew install mongodb-community@5.0

brew services stop mongodb-community@5.0

brew services list

mongosh
```

- To download and configure MongoDB CLI: https://docs.mongodb.com/mongocli/master/configure/#std-label-mcli-configure

```
mongocli config describe default
```

- To connect to a Remote Host: https://docs.mongodb.com/mongodb-shell/connect/#mongodb-instance-on-a-remote-host

```
 mongosh "mongodb+srv://USER:PASS@cluster0.9ptvo.mongodb.net/Bat_DB?retryWrites=true&w=majority"
```

---

### Commands

Some commands to remember for Aggregating data:

```
db.createCollection(
    "bat_test_collection", {
      timeseries: {
         timeField: "timestamp_ts"
       }
     }
)

db.bat_test_collection.aggregate([
  {
    $addFields: {
      timestamp_ts: {
        $dateFromString: {
          dateString: "$timestamp"
        }
      }
    }
  }
])
```
