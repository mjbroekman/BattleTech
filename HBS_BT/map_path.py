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

MAX_JUMP = 29.999

class BTmap:
    '''
    Class definition for constructing BattleTech transit map
    '''

    def __init__(self):
        self._load()
        self._find_jumps()

    def _load(self):
        '''
        Load the starsystem files to construct the map
        '''

        self.stars = {}
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
            self.stars[star]['x'] = data['Position']['x']
            self.stars[star]['y'] = data['Position']['y']
            self.stars[star]['z'] = data['Position']['z']
            self.stars[star]['diff'] = data['DefaultDifficulty']
            self.stars[star]['dist'] = data['JumpDistance']

            # Initialize the number of visits and neighbors.
            self.stars[star]['visits'] = 0
            self.stars[star]['neighbors'] = {}

    def _find_jumps(self):
        '''
        Find all the jump connections between starsystems
        '''
        s_iter1 = iter(self.stars)
        while True:
            try:
                star = next(s_iter1)
            except StopIteration:
                break

            s_iter2 = iter(self.stars)
            while True:
                try:
                    star2 = next(s_iter2)
                except StopIteration:
                    break

                if star == star2:
                    continue

                # Determine the 3-D distance between the systems.
                d_x = (self.stars[star]['x'] - self.stars[star2]['x']) ** 2
                d_y = (self.stars[star]['y'] - self.stars[star2]['y']) ** 2
                d_z = (self.stars[star]['z'] - self.stars[star2]['z']) ** 2
                threedimdist = (d_x + d_y + d_z) ** 0.5

                # If we are within the maximum jump distance and not already a neighbor, add it
                if threedimdist < MAX_JUMP and star2 not in self.stars[star]['neighbors']:
                    j_time = self.stars[star]['dist'] + self.stars[star2]['dist'] + 3
                    print('Adding neighbor ' + star2 + ' to ' + star +
                          ' at distance ' + str(threedimdist) + ' with duration ' +
                          str(j_time))
                    self.stars[star]['neighbors'][star2] = j_time
                    self.stars[star2]['neighbors'][star] = j_time

    def _has_neighbors(self, star):
        '''
        Return true or false depending on whether a star has any neighbors.
        For validating that the map is connected.
        '''
        neighbors = len(self.stars[star]['neighbors'].keys())
        if neighbors > 0:
            return True
        return False

    def _is_good_neighbor(self, star, neigh):
        '''
        Return true / false depending on whether a star & a neighbor are within 2 difficulty levels
        '''
        if self.stars[neigh]['diff'] == self.stars[star]['diff']:
            return True
        if self.stars[neigh]['diff'] > self.stars[star]['diff']:
            if self.stars[neigh]['diff'] < (self.stars[star]['diff'] + 4):
                return True
        if self.stars[star]['diff'] > self.stars[neigh]['diff']:
            if self.stars[star]['diff'] < (self.stars[neigh]['diff'] + 4):
                return True

        return False

    def _has_bad_neighbor(self, star):
        '''
        Checks neighbors for 'goodness'
        '''
        n_iter = iter(self.stars[star]['neighbors'])
        while True:
            try:
                neigh = next(n_iter)
            except StopIteration:
                break

            if not self._is_good_neighbor(star, neigh):
                print(star + ' (' + str(self.stars[star]['diff']) + ') and ' +
                      neigh + '(' + str(self.stars[neigh]['diff'])+ ') are not good neighbors')

    def get_path(self, start):
        '''
        Return the starsystem path from the specified starting point until all systems are visited.
        '''
        self.path_cost = 0
        self.path = []
        self.stars[start]['visits'] += 1

    def print_path(self):
        '''
        Print out the path to take
        '''
        print(self.path)

    def print_neighborhood(self):
        s_iter = iter(self.stars)
        while True:
            try:
                star = next(s_iter)
            except StopIteration:
                break

            self._has_bad_neighbor(star)

BT_MAP = BTmap()
BT_MAP.print_neighborhood()
#print(BT_MAP.get_path(sys.argv[0]))
