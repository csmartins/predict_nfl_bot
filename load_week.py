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


def do_main():
    if len(sys.argv) < 3:
        print("Missing parameters")
        print("Expected: python load_week.py <season> <week>")
        return

    season = sys.argv[1]
    week = sys.argv[2]

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '78dc11b4e6294b30a5fd268fc26c3e8c',
    }

    try:
        conn = http.client.HTTPSConnection('api.fantasydata.net')
        conn.request("GET", "/v3/nfl/scores/JSON/ScoresByWeek/{}/{}?%s".format(season, week), "", headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')

        data = json.loads(data)
        create_week_base_file(week, data)
        create_week_files_for_users(week)

        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__ == '__main__':
    do_main()