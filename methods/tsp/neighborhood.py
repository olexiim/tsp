#!/usr/bin/env python
"""Contains neighborhood implementations for the TSP problem.

There are several neighborhood classes:
    OnePointNeighborhood
    TwoPointNeighborhood
    TwoOptNeighborhood
Check their descriptions for more details

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

from methods.neighborhood import BasicNeighborhood
from numpy.random import randint

class OnePointNeighborhood(BasicNeighborhood):
    """One-point neighborhood for the TSP problem
    
    For a given state we randomly select a point (city). And then relocate the
    selected city to all other positions of the tour.
    For instance having a tour [0, 1, 2, 3, 4] and the selected city #2 we
    build next new states (tours):
        [2, 0, 1, 3, 4]
        [0, 2, 1, 3, 4]
        [0, 1, 3, 2, 4]
        [0, 1, 3, 4, 2]
    
    Attributes:
        Please refer to BasicNeighborhood class description
    """
    
    _name = "One-point move"
    _short_name = "One-point"
    _default = True
    
    def get_neighbors(self, state):
        """Returns a list of neighbor states for a state.
        
        See class description for details.
        
        Args:
            state:
            
        Returns:
            List of the states that are neighbors of the specified state 
            according to the one-point neighborhood strategy 
        """
        neighbors = []
        city_idx = randint(state.cities_num())
        cities_tmp = state._cities[:]
        city = cities_tmp.pop(city_idx)
        for pos in range(state.cities_num()):
            if pos!=city_idx:
                new_state = state.copy()
                new_state._cities[:] = cities_tmp[:]
                new_state._cities.insert(pos, city)
                neighbors.append(new_state)
        return neighbors
        
class TwoPointNeighborhood(BasicNeighborhood):
    """Two-point neighborhood for the TSP problem
    
    For a given state we randomly select a point (city). And then swap the 
    position of the selected city with each other city
    For instance having a tour [0, 1, 2, 3, 4] and the selected city #2 we
    build next new states (tours):
        [2, 1, 0, 3, 4]
        [0, 2, 1, 3, 4]
        [0, 1, 3, 2, 4]
        [0, 1, 4, 3, 2]
    
    Attributes:
        Please refer to BasicNeighborhood class description
    """
    
    _name = "Two-point move"
    _short_name = "Two-point"
    _default = False
    
    def get_neighbors(self, state):
        """Returns a list of neighbor states for a state.
        
        See class description for details.
        
        Args:
            state:
            
        Returns:
            List of the states that are neighbors of the specified state 
            according to the one-point neighborhood strategy 
        """
        neighbors = []
        city_idx = randint(state.cities_num())
        city = state._cities[city_idx]
        for pos in range(state.cities_num()):
            if pos!=city_idx:
                new_state = state.copy()
                new_state._cities[city_idx] = new_state._cities[pos]
                new_state._cities[pos] = city
                neighbors.append(new_state)
        return neighbors
        
class TwoOptNeighborhood(BasicNeighborhood):
    """Two-opt neighborhood for the TSP problem
    
    For a given state we randomly select an egde of the tour. Then for each
    other edge that do not have common seond point from the first edge and the
    first point from the second edge with the selected edge do:
        - take a part of tour between a second point of the first edge and
        a first point of the second edge
        - create a new tour with the taken part of tour reversed in place
    For instance having a tour [1, 2, 3, 4, 0] and the selected the edge (1, 2) 
    we build next new states (tours):
        For the second edge (3, 4) the middle part would be (2-3) so simply swap
        this two cities: [1, 3, 2, 4, 0]
        For the second edge (4, 0) the middle part would be (2-3-4) so reverse
        it and get a new tour: [1, 4, 3, 2, 0]
        For the third edge (0, 1) the middle part would be (2-3-4-0) so reverse
        it and get a new tour: [1, 0, 4, 3, 2]
    
    Attributes:
        Please refer to BasicNeighborhood class description
    """
    
    _name = "Two-opt move"
    _short_name = "Two-opt"
    _default = False
    
    def get_neighbors(self, state):
        """Returns a list of neighbor states for a state.
        
        See class description for details.
        
        Args:
            state:
            
        Returns:
            List of the states that are neighbors of the specified state 
            according to the one-point neighborhood strategy 
        """
        neighbors = []
        cities_num = state.cities_num()
        city_idx_1 = randint(cities_num)
        city_1 = state._cities[city_idx_1]
        city_idx_2 = (city_idx_1 + 1) % cities_num
        double_cities = 2*state._cities
        for i in range(cities_num-3):
            city_idx_3 = city_idx_2 + 1 + i
            city_idx_4 = city_idx_3 + 1
            new_state = state.copy()
            middle = double_cities[city_idx_2:city_idx_3+1]
            middle.reverse()
            new_state._cities[:] = [city_1] + middle[:] + double_cities[city_idx_4:city_idx_1+cities_num]
            neighbors.append(new_state)
        return neighbors