import http.client
import json
import time
import sys
import collections

# PART A

api_key = sys.argv[1]
url = "/3/discover/movie?language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&primary_release_date.gte=2004-01-01&with_genres=18"

#PART B
page_num = 1
movie_count = 350
temp_movie_count = movie_count

# API call code suggested by themoviedb.org
conn = http.client.HTTPSConnection("api.themoviedb.org")
movie_list = []

start_time = time.time()
api_call = 0 #count number of API calls

while temp_movie_count > 0: 
    api_call += 1
    url = url + "&page=" + str(page_num) + "&api_key=" + api_key
    payload = "{}"
    conn.request("GET", url, payload)
    res = conn.getresponse()
    data = res.read()
    movie_result = json.loads(data.decode("utf-8"))["results"]

    temp_movie_count = temp_movie_count - len(movie_result)
    if temp_movie_count > 0:
        movie_list.extend(movie_result)
    else:
        movie_list.extend(movie_result)
        movie_list = movie_list[0:movie_count]
    page_num += 1


# Create CSV
csv = open('movie_ID_name.csv', "w")
for movie in movie_list:
    title = movie["title"]
    if ',' in title: # add quote if there is comma
        title = title.replace("\"", "\"\"")
        title = "\"" + title + "\""
    line = str(movie["id"]) + ',' + title + "\n"
    csv.write(line)




#PART C SIMILAR MOVIE RETRIEVAL
url = "/3/movie/movie_id/similar?language=en-US&page=1"

related_movie_list = collections.OrderedDict()

conn = http.client.HTTPSConnection("api.themoviedb.org")

for movie in movie_list:
    movie_id = movie["id"]
    new_url = url.replace("movie_id",str(movie_id)) + "&api_key=" + api_key
    payload = "{}"

    elapse = time.time() - start_time
    if elapse >= 10:
        api_call = 0
        start_time = time.time()
    else:
        if api_call == 35:
            print("waiting ...")
            time.sleep(10-elapse)
            api_call = 0
            start_time = time.time()

    conn.request("GET", new_url, payload)

    api_call += 1
    print(api_call)
    res = conn.getresponse()
    data = res.read()
    movie_result = json.loads(data.decode("utf-8"))["results"]

    if movie_result is None:
        related_movie_list[movie_id] = []
    else:
        if len(movie_result) > 5:
            movie_result = movie_result[:5]
        related_movie_list[movie_id] = [i['id'] for i in movie_result]
    
# Remove Deplication
for movie_id in related_movie_list:
    for related_movie_id in related_movie_list[movie_id]:
        if related_movie_id in related_movie_list:

            if movie_id < related_movie_id:
                if movie_id in related_movie_list[related_movie_id]:
                    related_movie_list[related_movie_id].remove(movie_id) 
            else:
                if movie_id in related_movie_list[related_movie_id]:
                    related_movie_list[movie_id].remove(related_movie_id)
    
# Make csv
csv = open('movie_ID_sim_movie_ID.csv', "w")
for movie_id in related_movie_list:
    for related_movie_id in related_movie_list[movie_id]:
        line = str(movie_id) + ',' + str(related_movie_id) + "\n"
        csv.write(line)