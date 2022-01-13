# atlas-hackathon-time-series
💚 My submission for the Atlas Hackathon sponsored by MongoDB. This is a Time Series app.


There is an initiative where scientists track animal movements by attaching a GPS device to the animal, which then sends out a pulse in n number of frequencies.

This data is then stored on the Movebank database.

There is a public API which gets this data, so developers can use it in various ways.

What I am doing is this following:
    - Authenticate by logging in with credentials to Movebank
    - Use an HTTP GET Request to get the data from Movebank's public API.
        - Within my request's query string, I am specifying that I only want to GET data for X type of animal.
    - Convert this data to CSV and JSON format, for nice compatibility with Atlas Collections.

    - Now that I have the data I want in JSON, I can import this data into a MongoDB Atlas cluster.
    - I install mongoimport, then import this data from the command line.
