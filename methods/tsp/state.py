#!/usr/bin/env python
"""Contains state class for the TSP problem.

Contains class TspState that defines a state in the searching space of 
the TSP problem.

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

from copy import deepcopy
from methods.state import State
from numpy.random import shuffle

class TspState(State):
    """TspState class. Inherited from the State class.
    
    We use _cities property to store the travelling salesman tour. A tour is 
    stored in a list of N numbers that correspond to cities. City numbers are 
    going from 0 to N-1.
    
    For instance if we have N=5 cities then _cities could be:
        _cities = [0, 3, 2, 4, 1]
    
    Attributes:
        _cities: list of all queens row numbers
        _cities_num: number of cities
    """
    _cities = []
    _cities_num = 0
    
    def __init__(self, cities_num, is_empty=True):
        """Inits state with some tour.
        
        The simplest tour [0, 1, 2, ..., N-1] tour is used for init.
        
        Args:
            cities_num: number of cities
            is_empty: not used
        """
        self._cities_num = cities_num
        self._cities = [i for i in range(cities_num)]
        shuffle(self._cities)
            
    def random_generate(self, cities_num):
        """Generates random tour
        
        The state is filled with randomly shuffled list [0, 1, 2, ..., N-1]
        
        Args:
            cities_num: number of cities
        """
        state = self.__class__(cities_num, is_empty=False)
        shuffle(state._cities)
        return state
        
    def randomize(self):
        """Generates random tour
        
        Randomizes already existed tour
        """
        self._cities = [i for i in range(self._cities_num)]
        shuffle(self._cities)
        
    def copy_from(self, state):
        """Copies this state from the outer one"""
        self._cities[:] = state._cities[:]
            
    def cities_num(self):
        """Returns the number of cities"""
        return len(self._cities)
        
    def copy(self):
        """Returns a copy of this state"""
        return deepcopy(self)
        
    def __eq__(self, state):
        """Checks if a state is equal to this state"""
        return self._cities==state._cities
        
    def to_string(self):
        """Converts this state to string representation"""
        return str(self._cities)