#!/usr/bin/env python
"""Class module for storing TSP cities information

@author: Oleksii Molchanovskyi
@organization: Kyiv Polytechnic Institute
@country: Ukraine

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from numpy.random import random
from numpy import sqrt
from copy import deepcopy

MAP_SIZE = 1000

class TspBoard(object):
    _cities_num = 0
    _cities = []
    _distance = []
    _edges = {}
    
    def random(self, cities_num):
        self._cities = []
        self._cities_num = cities_num
        for c in range(cities_num):
            self._cities.append((MAP_SIZE*random(),MAP_SIZE*random()))
        self._calc_distancies()
        self._calc_edges()
        
    def load_from_file(self, filename):
        self._cities = []
        self._cities_num = 0
        try:
            with open(filename,'r') as f:
                self._cities_num = int(f.readline())
                for line in f:
                    x, y = tuple([float(x) for x in line.split()])
                    self._cities.append((x, y))
            self._calc_distancies()
            self._calc_edges()
        except IOError:
            # Cannot open file
            return False
        return True
        
    def save_to_file(self, filename):
        try:
            with open(filename,'w') as f:
                f.write(str(self._cities_num))
                map(lambda x: f.write("\n%.3f %.3f"%x), self._cities)
        except IOError:
            # Cannot open file
            return False
        return True                
            
    def _calc_distancies(self):
        self._distance = [[0 for x in range(self._cities_num)] for x in range(self._cities_num)]
        for i in range(self._cities_num-1):
            for j in range(i+1, self._cities_num):
                if i!=j:
                    self._distance[i][j] = self._distance[j][i] = sqrt((self._cities[i][0]-self._cities[j][0])**2 + (self._cities[i][1]-self._cities[j][1])**2)
                    
    def _calc_edges(self):
        self._edges = {}
        self._edges['max_x'] = max([x[0] for x in self._cities])
        self._edges['max_y'] = max([x[1] for x in self._cities])
        self._edges['min_x'] = min([x[0] for x in self._cities])
        self._edges['min_y'] = min([x[1] for x in self._cities])        
        
    def cities_num(self):
        return self._cities_num
        
    def cities(self):
        return self._cities
        
    def distance_matrix(self):
        return self._distance
        
    def max_x(self):
        return self._edges['max_x']
        
    def max_y(self):
        return self._edges['max_y']
        
    def min_x(self):
        return self._edges['min_x']
        
    def min_y(self):
        return self._edges['min_y']
        
    def copy(self):
        return deepcopy(self)