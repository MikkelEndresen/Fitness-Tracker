from pymongo import MongoClient

import json



config_file = open('config.json', 'r')
config = json.load(config_file)

uri = config['testcluster']

client = MongoClient(uri)

try:
    database = client.get_database("sample_mflix")
    movies = database.get_collection("movies")
    print(movies)
    # Query for a movie that has the title 'Back to the Future'
    query = { "title": "Back to the Future" }
    movie = movies.find_one(query)
    print(movie)
    client.close()


except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)

