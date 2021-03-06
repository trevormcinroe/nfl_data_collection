"""
This file should contain all functions


The stats data should be altered to a much cleaner version of itselfk
"""

import os
import json
from datetime import datetime
import pymongo
from pymongo import MongoClient
import configparser

top_dir = r'C:\Users\trevor_mcinroe\nfl'
bio_folder = 'profile_data'
stats_folder = 'stats_data'

# print(os.listdir(os.path.join(top_dir, bio_folder))[0])
amari = [x for x in os.listdir(os.path.join(top_dir, bio_folder)) if 'Amari' in x]
#
file = os.path.join(top_dir, bio_folder,
                   amari[0])
#
with open(file) as f:
    data = json.load(f)
# print(data['height'].split('-'))
# # print(type(str(data['current_team'])))
# dob = data['birth_date']
# print(dob)
# print(datetime.datetime.strptime(dob, '%Y-%m-%d'))


def write_to_db():
    """"""
    pass



def data_move():
    """"""
    pass



class DataManager:

    def __init__(self, top_dir,
                 bio_dir,
                 stats_dir,
                 db=None,
                 bio_collection=None,
                 stats_collection=None):

        self.top_dir = top_dir
        self.bio_dir = bio_dir
        self.stats_dir = stats_dir
        # self.db = db
        # self.bio_collection = bio_collection
        # self.stats_collection = stats_collection
        # self.creds = self._register()
        # self.mongo_connection  = self._make_connection()

    def _register(self):
        """"""

        parser = configparser.ConfigParser()

        parser.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'creds.ini'))

        return {
            'server_ip': parser['SERVER']['server_ip'],
            'server_port': parser['SERVER']['server_port'],
            'usr': parser['LOGIN']['usr'],
            'pwd': parser['LOGIN']['pwd']
        }

    def _make_connection(self):
        """
        This method creates connection to the MongoDB Server during the initalization of the class
        """

        client = pymongo.MongoClient(self.creds['server_ip'],
                                     int(self.creds['server_port']))

        return client

    def _write_to_db(self, collection, data):
        """

        Args:
            collection:
            data:

        Returns:

        """

        db = self.mongo_connection[self.db]

        db.authenticate(name=self.creds['usr'],
                        password=self.creds['pwd'])

        col = db[collection]

        col.insert_many(data)

    def _player_bio(self, player_list):
        """

        Args:
            player_list: a list of .json files from the profile_data folder

        Returns:

        """

        data_container = []

        for player in player_list:
            # The first thing we need to do is open the file..
            file = os.path.join(self.top_dir,
                                self.bio_dir,
                                player)
            with open(file) as f:
                data = json.load(f)

            # Now, we really don't need old-ass players that aren't on the field anymore
            try:
                if datetime.strptime(data['birth_date'], '%Y-%m-%d') < datetime.strptime('1970-01-01', '%Y-%m-%d'):
                    continue
            except:
                pass
            try:
                if datetime.strptime(data['death_date'], '%Y-%m-%d') < datetime.strptime('1980-01-01', '%Y-%m-%d'):
                    continue
            except:
                pass

            # Now that we have the data, we need to manipulate a few things
            # (1) Height data is in foot-inch format. In order to make this info palpable for
            # a mathematical model, it needs to be entirely numerical. Let's convert to inches
            try:
                height = data['height'].split('-')
                data['height'] = int(height[0])*12 + int(height[1])
            except:
                pass

            # To make data querying more convenient during runtime of the ultimate models,
            # we should be able to query these player stats by team
            new_data = dict()
            new_data[str(data['current_team'])] = data
            data_container.append(new_data)

        self._write_to_db(collection=self.bio_collection, data=data_container)

    def _player_stats(self, player_list):
        """"""

        data_container = []

        for player in player_list:
            file = os.path.join(self.top_dir,
                                self.stats_dir,
                                player)

            # This data is structured as a list of dicts where there is one dict per game that
            # the player has played in their career
            with open(file) as f:
                data = json.load(f)

            # Pulling out the player_id from one of the dicts in the list
            try:
                new_data = dict()
                new_data[str(data[0]['player_id'])] = data
                data_container.append(new_data)
            except:
                continue

        self._write_to_db(collection=self.stats_collection, data=data_container)



import time
a = DataManager(top_dir=top_dir, bio_dir=bio_folder, stats_dir=stats_folder)

start = time.time()
player_list = os.listdir(os.path.join(a.top_dir, a.bio_dir))
stats_list = os.listdir(os.path.join(a.top_dir, a.stats_dir))
a._player_bio(player_list=player_list)

print(f'{(time.time() - start)/60} minutes.')

start = time.time()
a._player_stats(player_list=stats_list)
print(f'{(time.time() - start)/60} minutes.')