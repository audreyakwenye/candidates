
def get_trends():
    results = TWITTER.trends_place(id = 23424977)
    trends = []
    for location in results:
        for trend in location["trends"]:
            trend = trend["name"]
        trends.append(trend)
    return(trends)