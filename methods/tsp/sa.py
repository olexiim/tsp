#!/usr/bin/env python
"""Contains a class that implements Simulated Annealing method for the TSP.

Class SimulatedAnnealing tries to solve the TSP problem with Simulated 
Annealing metaheuristic searching method. Tabu is inherited from BasicMethod.

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
from numpy.random import shuffle, random
from numpy import exp

class SimulatedAnnealing(BasicMethod):
    """Simulated Annealing metaheuristic method implementation for the TSP.
    
    The class reimplements BasicMethod.run function.

    Attributes:
        _time_max: maximum time of annealing process
        _temp_max: maximum temperature of annealing
        For other attributes please refer BasicMethod class description.  
    """
    
    _name = "Simulated annealing"
    _short_name = "SA"
    _type = "Metaheuristic"
    _time_max = 1000
    _temp_max = 10000
    
    def _temperature(self, t):
        """Calulcates temperature based on time t"""
#        print t, self._time_max, self._temp_max
        T = t*float(-self._temp_max)/self._time_max + self._temp_max
        if T<0:
            return 0
        return T
    
    def _probability(self, delta, t):
        """Returns probability of acceptance of a difference between two states
        
        Args:
            delta: difference between costs of two state (tours)
            t: running time (in amount of iterations)
            
        Returns:
            Probability value from 0 to 1
        """
        if delta<0:
            print delta, t, "1"
            return 1
        else:
            T = self._temperature(t)
            if T<=0:
                return 0
            P = exp(-delta/T)
            print delta, t, P, T
            if P>1:
                P = 1
            elif P<0:
                P = 0
            return P
    
    def run(self, input_state, stat=StatRecord()):
        """Runs simulated annealing strategy to solve the TSP problem.
        
        Args:
            Please refer to BasicMethod.run description
            
        Returns:
            Please refer to BasicMethod.run description
        """
        start_time = time()
        super(SimulatedAnnealing, self).run(input_state, stat)
        
        self._tabu_list_limit = input_state.cities_num()*100
        ever_found_best_state = input_state.copy()
        state, value = input_state.copy(), self.calc_solution_cost(input_state)
        stat.solution_cost = value
        t = 0
        self._temp_max = value
        while(True):
#            print '{:.2f}'.format(value)
            self.send_current_cost(value, stat.solution_cost)
            if time()-start_time > self._run_time_limit:
                return ever_found_best_state, "Run time limit has been reached"
                
            new_states = self.get_neighbors(state)
            shuffle(new_states)
            best_state, best_value = None, float('inf')
            for new_state in new_states:
                v = self.calc_solution_cost(new_state)
                if self._probability(v - value, t)>random():
                    best_state, best_value = new_state, v
                    break
            if not best_state:
                break
            
            t += 1
            
            state, value = best_state, best_value
            self.send_state(state, value)
#            print state, value
            if value<stat.solution_cost:
                ever_found_best_state.copy_from(state)
                stat.solution_cost = value
                self.send_best_state(ever_found_best_state, value, stat)
            
            stat.overall_nodes_generated += len(new_states)
            stat.overall_run_time = time() - start_time
            
        return ever_found_best_state, "Local optimum is reached"