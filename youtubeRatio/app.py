import requests
import json
import math
import itertools

API_KEY = 'AIzaSyAPcClOc9h2LHjFLZ--ZxVfQXt3tNJ_s9w'

videoId = []
good = []
bad = []


@app.route('/search', methods=['POST'])
def search():
    channel_right = request.form.get('channel_right')
    def get_channel_id():
        url = f'https://www.googleapis.com/youtube/v3/channels?part=id&forUsername={channel_right}&key={API_KEY}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data["items"][0]["id"]
        except:
            data = None
        return data

    if get_channel_id() == None:
        channel_url = request.form.get('channel_right')
    else:
        channel_url = get_channel_id()

    def get_channel_name():
        url = f'https://www.googleapis.com/youtube/v3/search?type=channel&part=snippet&q={channel_url}&key={API_KEY}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data["items"][0]["snippet"]["channelTitle"]
        except:
            data = None
        return data

    def get_totalResults():
        url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_url}&key={API_KEY}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data["pageInfo"]["totalResults"]
        except:
            data = None
        return data

    totalResults = get_totalResults()
    count = math.ceil(int(totalResults)/5)

    for i in range(5):
        url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UC2v99T3RRi5NkdhP0ZqdpXA&key={API_KEY}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        data = data["items"][i]["id"]["videoId"]
        videoId.append(data)

    def get_nextPageToken():
        url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_url}&key={API_KEY}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data["nextPageToken"]
        except:
            data = None
        return data

    nextPageToken = get_nextPageToken()

    for i in range(count):
        for i in range(5):
            url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_url}&key={API_KEY}&pageToken={nextPageToken}'
            json_url = requests.get(url)
            data = json.loads(json_url.text)
            try:
                data = data["items"][i]["id"]["videoId"]
            except:
                data = None
            videoId.append(data)
        def get_anotherPageToken():
            url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_url}&key={API_KEY}&pageToken={nextPageToken}'
            json_url = requests.get(url)
            omoi = json.loads(json_url.text)
            try:
                omoi = omoi["nextPageToken"]
            except:
                omoi = None
            return omoi
        nextPageToken = get_anotherPageToken()

    for i in range(100):
        try:
            videoId.remove(None)
        except ValueError:
            break

    for video in videoId:
        url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video}&key={API_KEY}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        data = data["items"][0]["statistics"]["likeCount"]
        good.append(data)

    for video in videoId:
        url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video}&key={API_KEY}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        data = data["items"][0]["statistics"]["dislikeCount"]
        bad.append(data)

    good2 = [int(s) for s in good]
    dic = {key: val for key, val in zip(videoId, good2)}
    dic2 = sorted(dic.items(), key=lambda x:x[1], reverse=True)
    last_good  = list(itertools.chain.from_iterable(dic2))[0::2]

    bad2 = [int(s) for s in bad]
    dic3 = {key: val for key, val in zip(videoId, bad2)}
    dic4 = sorted(dic3.items(), key=lambda x:x[1], reverse=True)
    last_bad  = list(itertools.chain.from_iterable(dic4))[0::2]


    return render_template(
        'users.html',
        channel_name = get_channel_name(),
        bad1 = last_bad[0],
        bad2 = last_bad[1],
        bad3 = last_bad[2],
        good1 = last_good[0],
        good2 = last_good[1],
        good3 = last_good[2]
        # goodratio1 = goodratio1,
        # goodratio2 = goodratio2,
        # goodratio3 = goodratio3,
        # badratio1 = badratio1,
        # badratio2 = badratio2,
        # badratio3 = badratio3,
        # allgood1 = allgood1,
        # allgood2 = allgood2,
        # allgood3 = allgood3,
        # allbad1 = allbad1,
        # allbad2 = allbad2,
        # allbad3 = allbad3
    )




if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')