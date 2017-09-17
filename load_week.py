import sys, json, os
from fantasy import FantasyConnection

users_list = ['csmartins', 'douglasrhx', 'lbalabram', 'leozinho420', 'guru_mikonha', 'Carekaled', 'T_maskot']


def create_directory(path):
    if not (os.path.isdir(path)):
        os.mkdir(path)


def create_week_base_file(week, data):
    create_directory(week)

    with open(week + '/week-' + week + '.json', 'w') as data_file:
        json.dump(data, data_file)


def create_week_files_for_users(week):
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

    scores = {}
    with open(week + '/week-' + week + '.json') as data_file:
        games = json.load(data_file)
        for game in games:
            d = {'AwayScore': game['AwayScore'], 'HomeScore': game['HomeScore']}
            if game['HomeScore'] is not None:
                if int(game['HomeScore']) > int(game['AwayScore']):
                    d['Winner'] = game['HomeTeam']
                else:
                    d['Winner'] = game['AwayTeam']

            scores[game['GameKey']] = d

    with open(week + '/week-' + week + '-scores.json', 'w') as data:
        json.dump(scores, data)


def count_scores_by_users(week):
    create_directory(week)

    users_scores = {}
    with open(week + '/week-' + week + '-scores.json') as scores_file:
        scores = json.load(scores_file)
        for user in users_list:
            with open(week + '/' + user + '.json') as user_games:
                users_predicts = json.load(user_games)
                total_score = 0
                for game in users_predicts:
                    if game['predicted'] and game['predict'] == scores[game['GameKey']]['Winner']:
                        total_score += 1
                users_scores[user] = total_score
    
    with open(week + '/users_scores.json', 'w') as data:
        json.dump(users_scores, data)


def do_main():
    if len(sys.argv) < 4:
        print("Missing parameters")
        print("Expected: python load_week.py <season> <week> <param>")
        return

    season = sys.argv[1]
    week = sys.argv[2]
    param = sys.argv[3]

    try:
        fantasy = FantasyConnection()
        data = fantasy.get_scores_by_week(season, week)

        if param == 'all':
            create_week_base_file(week, data)
            create_week_files_for_users(week)
            create_scores_file(week)
            count_scores_by_users(week)

        elif param == 'week':
            create_week_base_file(week, data)

        elif param == 'scores':
            create_week_base_file(week, data)
            create_scores_file(week)
            count_scores_by_users(week)

        elif param == 'users':
            create_week_files_for_users(week)

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__ == '__main__':
    do_main()
