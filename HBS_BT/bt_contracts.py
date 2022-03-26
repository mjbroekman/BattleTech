#!/usr/bin/env python3
'''
Module to determine transit paths from any given starsystem.
A 'transit path' is a series of jumps that will cover all starsystems in less than 1200 days

Author: Maarten Broekman
Inspired by ninte000's map work here:
    https://forum.paradoxplaza.com/forum/index.php?threads/career-mode-final-score-travel-route-and-thoughts.1144098/

'''

import copy
import itertools
import json
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from os import listdir
from os.path import expanduser, isdir, isfile, join
from platform import system

class BTcontracts:
    '''
    Class definition for constructing BattleTech contract map
    '''

    def __init__(self):
        self._load()

    def _load(self):
        '''
        Load the starsystem files to construct the map
        '''

        self.stars = {}
        self.factions = {}

        self.dir = "."

        if system() == 'Darwin':
            bt_dir = expanduser('~/Library/Application Support/Steam/SteamApps/common/BATTLETECH/')
            bt_dir = expanduser(bt_dir + 'BattleTech.app/Contents/Resources/Data/StreamingAssets/')
            if isdir(bt_dir):
                self.dir = bt_dir+'data/starsystem/'

        files = [f for f in listdir(self.dir) if isfile(join(self.dir, f))]

        for file in files:
            star_file = open(self.dir+file, 'r')
            star_data = star_file.read()
            data = json.loads(star_data)
            star = join(data['Description']['Name'], "").replace('/', '').replace(u'\xda', 'U')

            # Add the starsystem to the map.
            self.stars[star] = {}
            self.stars[star]['employer'] = {}
            self.stars[star]['target'] = {}
            for employ in data['ContractEmployers']:
                self.stars[star]['employer'][employ] = 1
                self.factions[employ] = 1

            for target in data['ContractTargets']:
                self.stars[star]['target'][target] = 1
                self.factions[target] = 1

    def _find_faction_jobs(self, faction):
        '''
        Find the jobs for a particular faction
        '''
        s_iter = iter(self.stars)

        employer = "\n"
        target = "\n"
        while True:
            try:
                star = next(s_iter)
            except StopIteration:
                break

            if faction in self.stars[star]['employer']:
                employer = "\n\t\t" + star + employer

            if faction in self.stars[star]['target']:
                target = "\n\t\t" + star + target

        return faction + ":\n\tEmployer:" + employer + "\n\tTarget:" + target

    def find_jobs(self):
        '''
        Find all the jobs
        '''
        f_iter = iter(self.factions)

        while True:
            try:
                faction = next(f_iter)
            except StopIteration:
                break

            print(self._find_faction_jobs(faction))

BT_MAP = BTcontracts()
BT_MAP.find_jobs()
#print(BT_MAP.get_path(sys.argv[0]))
