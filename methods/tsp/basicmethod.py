#!/usr/bin/env python
"""Contains a basic class BasicMethod for the methods for the TSP problem.

Class BasicMethod is inherited from Method class. As we have several methods
for the TSP and these methods have something similar corresponding to
the problem it's better to combine this general behavior into one common class.

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

from methods.statrecord import StatRecord
from methods.method import Method

class BasicMethod(Method):
    """Base class for search methods for the N-queens problem.
    
    The class reimplements following functions:
        __init__
        run
        calc_solution_cost

    Attributes:
        _distance_matrix: stores a distance matrix for TSP
            Distance matrix for N cities TSP problem is a NxN matrix each cell
            [i,j] of which stores distance from city @i to city @j
        For other attributes please refer to Method class description.
    """
    
    _name = "Basic method"
    _short_name = "Basic"
    _type = "Undefined"
    _run_time_limit = 60
    _distance_matrix = None
    
    def __init__(self, neighborhood=None, time_limit=None, args=None):
        super(BasicMethod, self).__init__(neighborhood, time_limit, args)
        self._distance_matrix = args[0]
    
    def run(self, initial_state, stat=StatRecord()):
        """Runs the method.
        
        Main function of the BasicMethod class. It just calls the parent
        class function and stores one common data to the statistics object.
        
        Args:
            Please refer to Method.run description
            
        Returns:
            Please refer to Method.run description
        """
        super(BasicMethod, self).run(initial_state, stat)
        stat.problem = "TSP for " + str(initial_state.cities_num()) + " cities"
        return initial_state, "We do nothing"
        
    def calc_solution_cost(self, state):
        """Returns distance of a tour that is described by state.
        
        Args:
            state: input state
            
        Returns:
            Total distance of a tour. 
            So if we have a state [0, 3, 1, 2] it means we have a tour
            0 - 3 - 1 - 2 - 0. The total distance would be:
                d[0][3] + d[3][1] + d[1][2] + d[2][0], 
                where d is a distance matrix self._distance_matrix
        """
        cost = 0
        prev_city = state._cities[state.cities_num()-1]
        for next_city in state._cities:
            cost += self._distance_matrix[prev_city][next_city]
            prev_city = next_city
        return cost