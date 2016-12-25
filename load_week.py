import http.client, urllib.error, sys, urllib.parse, json, os


def create_directory(path):
    if not (os.path.isdir(path)):
        os.mkdir(path)


def create_week_base_file(week, data):
    create_directory(week)

    with open(week + '/week-' + week + '.json', 'w') as data_file:
        json.dump(data, data_file)


def create_week_files_for_users(week):
    users_list = ['csmartins', 'douglasrhx', 'lbalabram', 'leozinho420', 'guru_mikonha', 'Carekaled', 'T_maskot']

    create_directory(week)

    with open(week + '/week-' + week + '.json') as data_file:
        games = json.load(data_file)
        users_predict = []
        for game in games:
            d = {'GameKey': game['GameKey'], 'AwayTeam': game['AwayTeam'], 'HomeTeam': game['HomeTeam'], 'predicted': False}
            users_predict.append(d)

        for user in users_list:
            with open(week + '/' + user + '.json', 'w') as user_games:
                json.dump(users_predict, user_games)


def create_scores_file(week):
    create_directory(week)

    scores = []
    with open(week + '/week-' + week + '.json') as data_file:
        games = json.load(data_file)
        for game in games:
            d = {'GameKey': game['GameKey'], 'AwayScore': game['AwayScore'], 'HomeScore': game['HomeScore']}
            if game['HomeScore'] != None:
                if int(game['HomeScore']) > int(game['AwayScore']):
                    d['Winner'] = game['HomeTeam']
                else:
                    d['Winner'] = game['AwayTeam']

            scores.append(d)

    with open(week + '/week-' + week + '-scores.json', 'w') as data:
        json.dump(scores, data)


def do_main():
    if len(sys.argv) < 5:
        print("Missing parameters")
        print("Expected: python load_week.py <season> <week> <subscription-key> <param>")
        return

    season = sys.argv[1]
    week = sys.argv[2]
    key = sys.argv[3]
    param = sys.argv[4]
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': key,
    }

    try:
        conn = http.client.HTTPSConnection('api.fantasydata.net')
        conn.request("GET", "/v3/nfl/scores/JSON/ScoresByWeek/{}/{}?%s".format(season, week), "", headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')

        data = json.loads(data)

        if param == 'all':
            create_week_base_file(week, data)
            create_week_files_for_users(week)
            create_scores_file(week)

        elif param == 'week':
            create_week_base_file(week, data)

        elif param == 'scores':
            create_scores_file(week)

        elif param == 'users':
            create_week_files_for_users(week)

        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__ == '__main__':
    do_main()
