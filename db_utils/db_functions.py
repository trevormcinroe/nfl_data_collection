"""
This file should contain all functions


The stats data should be altered to a much cleaner version of itselfk
"""

import os
import json


top_dir = r'C:\Users\trevor_mcinroe\nfl'
bio_folder = 'profile_data'
stats_folder = 'stats_data'

# print(os.listdir(os.path.join(top_dir, bio_folder))[0])
# file = os.path.join(top_dir, bio_folder,
#                    os.listdir(os.path.join(top_dir, bio_folder))[100])

# with open(file) as f:
#     data = json.load(f)
# print(data['height'].split('-'))
# print(type(str(data['current_team'])))
# print(data)



def write_to_db():
    """"""
    pass



def data_move():
    """"""
    pass



class DataManager:

    def __init__(self, top_dir, bio_dir, stats_dir):
        self.top_dir = top_dir
        self.bio_dir = bio_dir
        self.stats_dir = stats_dir

    def _player_bio(self, player_list):
        """

        Args:
            player_list: a list of .json files from the profile_data folder

        Returns:

        """

        for player in player_list:
            # The first thing we need to do is open the file..
            file = os.path.join(self.top_dir,
                                self.bio_dir,
                                player)
            with open(file) as f:
                data = json.load(f)

            # Now that we have the data, we need to manipulate a few things
            # (1) Height data is in foot-inch format. In order to make this info palpable for
            # a mathematical model, it needs to be entirely numerical. Let's convert to inches
            height = data['height'].split('-')
            data['height'] = int(height[0])*12 + int(height[1])

            # To make data querying more convenient during runtime of the ultimate models,
            # we should be able to query these player stats by team
            new_data = dict()
            new_data[str(data['current_team'])] = data

            print(new_data)



a = DataManager(top_dir=top_dir, bio_dir=bio_folder, stats_dir=stats_folder)

a._player_bio(player_list=os.listdir(
    os.path.join(a.top_dir, a.bio_dir)
)[:5])