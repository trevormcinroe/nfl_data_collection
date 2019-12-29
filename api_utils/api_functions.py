"""

"""

import nflgame
import nflgame.player as nfp
import pandas as pd

# This function returns a list of game objects
# games = nflgame.games(2018, week=1)
#
# print(games)



#####################
# Player-level stats#
#####################
player_dict = nfp._create_players(jsonf=nfp._player_json_file)
# print(player_dict)
# print(len(player_dict))

# pids = [k for k, v in player_dict.items()]
# for pid in pids:
#     print(f'{pid}: {player_dict[pid].name}')
# Each key returns a player object

# # The .stats() method returns a GamePLayerStats Class
# print(player_dict['00-0035717'].position)
stats = player_dict['00-0035717'].stats(year=2019, week=5)

print(stats.__dict__.keys())
player_stat_lists = []
for pid in [x for x in player_dict.keys()]:
    if not player_dict[pid].stats(year=2019, week=1).__dict__.keys() in [x for x in player_stat_lists]:
        player_stat_lists.append(player_dict[pid].stats(year=2019, week=1).__dict__.keys())
    else:
        continue

print(len(player_stat_lists))
print(player_stat_lists)


# a = [1, 2, 3]
# b = [4, 5, 6]
# c = [[1, 2, 3], [6, 7, 8]]
# if a in [x for x in c]:
#     print('here')


# print(dir(stats))
# print('----------------')
# print(stats._stats)
# print('----------------')
# print(stats.games)
# print('----------------')
# print(stats.formatted_stats())
# print('----------------')
# print('----------------')
# print('----------------')
# print('----------------')
# print('----------------')
# print('----------------')


def get_player_info():
    """"""
    # Creating a list of the data that we want to capture on the players. Then, using this list to
    # init an empty DataFrame
    var_list = ['player_id', 'first_name', 'last_name', 'team', 'position', 'uniform_number',
                'birthdate', 'college', 'height', 'weight', 'years_pro', 'status']
    df_master = pd.DataFrame(columns=var_list)

    # Gathering a dictionary of players from the players.json file within the nflgames package
    player_dict = nfp._create_players(jsonf=nfp._player_json_file)

    # All of the ditctionary keys are the player_ids
    for pid in [k for k, v in player_dict.items()]:
        df_holder = pd.DataFrame([player_dict[pid].player_stats()],
                                 columns=var_list)
        df_master = df_master.append(df_holder, ignore_index=True)

    # player_id, name_first, name_last, position, team, height, weight, years_pro, status
    return df_master

# Status codes
status_codes = {
    'ACT': 'active',
    'RES': 'injury_reserve',
    'NON': 'non_injury_out',
    'SUS': 'suspended',
    'PUP': 'physically_unable',
    'UDF': 'unsigned_draft_pick',
    'EXE': 'exempy'
}

##############
# Team Stats #
##############
