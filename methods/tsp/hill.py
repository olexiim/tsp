#!/usr/bin/env python
"""Contains the classes that implement local search methods for the TSP problem.

Several class that are inherited from BasicMethod and implement local search
strategies are provided in this module:
    HillClimbing: Hill climbing 
    HillClimbingWithSideMoves: Hill climbing with side moves
    RandomHillClimbing: Random hill climbing

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
from numpy.random import randint, random

class HillClimbing(BasicMethod):
    """Hill climbing local search method implementation for the TSP problem.
    
    The class reimplements BasicMethod.run function.

    Attributes:
        Please refer to BasicMethod class description    
    """
    
    _name = "Hill climbing"
    _short_name = "Hill climbing"
    _type = "Local"
    
    def run(self, input_state, stat=StatRecord()):
        """Runs Hill climbing local search strategy to solve the TSP problem.
        
        Args:
            Please refer to BasicMethod.run description
            
        Returns:
            Please refer to BasicMethod.run description
        """
        start_time = time()
        super(HillClimbing, self).run(input_state, stat)
        
        ever_found_best_state = input_state.copy()
        state, value = input_state.copy(), self.calc_solution_cost(input_state)
        stat.solution_cost = value
        while True:
#            print '{:.2f}'.format(value)
            self.send_current_cost(value, stat.solution_cost)
            if time()-start_time > self._run_time_limit:
                return ever_found_best_state, "Run time limit has been reached"
                
            new_states = self.get_neighbors(state)
            best_state, best_value = None, float('inf')
            for new_state in new_states:
                v = self.calc_solution_cost(new_state)
                if v<best_value and v<value:
                    best_state, best_value = new_state, v
                    
            if not best_state:
                break
            
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
        
class HillClimbingWithSideMoves(BasicMethod):
    """Hill climbing with side moves local search method implementation for TSP.
    
    The class reimplements BasicMethod.run function.

    Attributes:
        Please refer to BasicMethod class description    
    """
    
    _name = "HC with side moves"
    _short_name = "HC + side moves"
    _type = "Local"
    _disabled = True
    
    def run(self, input_state, stat=StatRecord()):
        """Runs Hill with side moves search strategy to solve the TSP problem.
        
        Args:
            Please refer to BasicMethod.run description
            
        Returns:
            Please refer to BasicMethod.run description
        """
        start_time = time()
        super(HillClimbingWithSideMoves, self).run(input_state, stat)
        
        ever_found_best_state = input_state.copy()
        state, value = input_state.copy(), self.calc_solution_cost(input_state)
        stat.solution_cost = value
        while(True):
#            print '{:.2f}'.format(value)
            self.send_current_cost(value, stat.solution_cost)
            if time()-start_time > self._run_time_limit:
                return ever_found_best_state, "Run time limit has been reached"
                
            new_states = self.get_neighbors(state)
            
            #
            # TODO: Write your implementation of the 
            # Hill climbing local search method with side moves
            #
            
            self.send_state(state, value)
#            print state, value
            if value<stat.solution_cost:
                ever_found_best_state.copy_from(state)
                stat.solution_cost = value
                self.send_best_state(ever_found_best_state, value, stat)
            
            stat.overall_nodes_generated += len(new_states)
            stat.overall_run_time = time() - start_time
            
        return ever_found_best_state, "Local optimum is reached"
        
class RandomHillClimbing(BasicMethod):
    """Random hill climbing local search method implementation for the TSP.
    
    The class reimplements BasicMethod.run function.

    Attributes:
        Please refer to BasicMethod class description    
    """
    
    _name = "Random hill climbing"
    _short_name = "Random HC"
    _type = "Local"
    _disabled = True
    
    def run(self, input_state, stat=StatRecord()):
        """Runs random hill climbing local search strategy to solve the TSP
        
        Args:
            Please refer to BasicMethod.run description
            
        Returns:
            Please refer to BasicMethod.run description
        """
        start_time = time()
        super(RandomHillClimbing, self).run(input_state, stat)
        
        ever_found_best_state = input_state.copy()
        state, value = input_state.copy(), self.calc_solution_cost(input_state)
        stat.solution_cost = value
        while(True):
#            print '{:.2f}'.format(value)
            self.send_current_cost(value, stat.solution_cost)
            if time()-start_time > self._run_time_limit:
                return ever_found_best_state, "Run time limit has been reached"
            
            new_states = self.get_neighbors(state)
            
            #
            # TODO: Write your implementation of the 
            # Random hill climbing local search method with side moves
            # Use randint or random functions for randomize stuff
            # Refer to help(numpy.random.randint) and help(numpy.random.random)
            #
            
            self.send_state(state, value)
#            print state, value
            if value<stat.solution_cost:
                ever_found_best_state.copy_from(state)
                stat.solution_cost = value
                self.send_best_state(ever_found_best_state, value, stat)
            
            stat.overall_nodes_generated += len(new_states)
            stat.overall_run_time = time() - start_time
            
        return ever_found_best_state, "Local optimum is reached"