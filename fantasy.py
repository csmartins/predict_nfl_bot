import os
import http.client
import json


class FantasyConnection:

    def __init__(self):
        self.subscription_key = os.environ['SUBSCRIPTION_KEY']
        self.headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.subscription_key,
        }
        self.conn = http.client.HTTPSConnection('api.fantasydata.net')

    def get_scores_by_week(self, season, week):
        self.conn.request("GET", "/v3/nfl/scores/JSON/ScoresByWeek/{}/{}?%s".format(season, week), "", self.headers)
        response = self.conn.getresponse()
        data = response.read().decode('utf-8')

        data = json.loads(data)

        return data

    def get_current_week(self):
        self.conn.request("GET", "/v3/nfl/stats/JSON/CurrentWeek", "{body}", self.headers)
        response = self.conn.getresponse()
        data = response.read().decode('utf-8')

        data = json.loads(data)

        return data

    def get_current_season(self):
        self.conn.request("GET", "/v3/nfl/stats/JSON/CurrentSeason", "{body}", self.headers)
        response = self.conn.getresponse()
        data = response.read().decode('utf-8')

        data = json.loads(data)

        return data

fantasy = FantasyConnection()
print(fantasy.get_scores_by_week(2017, 2))
