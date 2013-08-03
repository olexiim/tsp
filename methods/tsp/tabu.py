#!/usr/bin/env python
"""Contains a class that implements Tabu method for the TSP problem.

Class Tabu tries to solve the TSP problem with Tabu metaheuristic 
searching method. Tabu is inherited from BasicMethod.

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

from basicmethod import BasicMethod
from methods.statrecord import StatRecord
from time import time
from numpy.random import randint

class Tabu(BasicMethod):
    """Tabu metaheuristic method implementation for the TSP problem.
    
    The class reimplements BasicMethod.run function.

    Attributes:
        _tabu_list: list of the states that are prohibited to access
        _tabu_list_limit: maximum size of the tabu list; if it's overstated 
            than the oldest state is drop out from the list
        For other attributes please refer BasicMethod class description.  
    """
    
    _name = "Tabu"
    _short_name = "Tabu"
    _type = "Metaheuristic"
    _tabu_list = []
    _tabu_list_limit = 1000
    
    def _in_tabu(self, state):
        """Checks if the state in the tabu list"""
        for tabu_state in self._tabu_list:
            if tabu_state.__eq__(state):
                return True
        return False
    
    def run(self, input_state, stat=StatRecord()):
        """Runs Tabu strategy to solve the TSP problem.
        
        Args:
            Please refer to BasicMethod.run description
            
        Returns:
            Please refer to BasicMethod.run description
        """
        start_time = time()
        super(Tabu, self).run(input_state, stat)
        
        self._tabu_list_limit = input_state.cities_num()*100
        ever_found_best_state = input_state.copy()
        state, value = input_state.copy(), self.calc_solution_cost(input_state)
        stat.solution_cost = value
        while(True):
#            print '{:.2f}'.format(value)
            self.send_current_cost(value, stat.solution_cost)
            if time()-start_time > self._run_time_limit:
                return ever_found_best_state, "Run time limit has been reached"
                
            new_states = self.get_neighbors(state)
            best_states, best_value = [], float('inf')
            for new_state in new_states:
                v = self.calc_solution_cost(new_state)
                if v<=best_value and not self._in_tabu(new_state):
                    if v<best_value:
                        best_states = []
                    best_states.append(new_state)
                    best_value = v
                    
            if not best_states:
                break
            
            state = best_states[randint(len(best_states))] 
            value = best_value
            self.send_state(state, value)
            if len(self._tabu_list)==self._tabu_list_limit:
                self._tabu_list.pop()
            self._tabu_list.append(state)
#            print state, value
            if value<stat.solution_cost:
                ever_found_best_state.copy_from(state)
                stat.solution_cost = value
                self.send_best_state(ever_found_best_state, value, stat)
            
            stat.overall_nodes_generated += len(new_states)
            stat.overall_run_time = time() - start_time
            
        return ever_found_best_state, "Local optimum is reached"