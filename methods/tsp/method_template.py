#!/usr/bin/env python
"""This module includes a method template for the TSP problem.

@author: 
@organization: 
@country: 

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

class NewMethod(BasicMethod):
    """Template class for a new method that solves the TSP problem.

    Attributes:
        _name: title of the method
        _short_name: shorter title 
        _type: method type (e.g. informed, local, etc.)
        _run_time_limit: amount of seconds that method can work
        _neighborhood: neighborhood object (used in get_neighbors function)
        _disabled: if True then method will not be active in GUI
        _connection: Pipe connection to send information packages to the
            main application
        _distance_matrix: stores a distance matrix for TSP
            Distance matrix for N cities TSP problem is a NxN matrix each cell
            [i,j] of which stores distance from city @i to city @j
    """
    
    #
    # Please fill the description information below:
    #   name, short_name and type
    #   type could be ""Local", "Metaheuristic", etc.
    #
    _name = "New empty method"
    _short_name = "New method"
    _type = "Unknown"
    
    #
    # Change to _disabled = False to enable your method in a methods' list
    #
    _disabled = True
    
    def run(self, input_state, stat=StatRecord()):
        """Method's run function that does all work.
        
        During method's work you should do several mandatory things:
            1. Collect statistical information.
            2. Check the timer.
            3. Save a best found state and its cost value
            4. Send to the main program new found state and its cost
            5. Send to the main program new found best state and its cost
        Please read the comments in the source code below for details.
        
        Args:
            input_state: initial state of the problem
            stat: object of type StatRecord that fill store all statistics
            
        Returns:
            Result of the method call in format [State, Message], where
            first parameter stores an ever found best state, while the 
            second parameter contains additional message in string format
            for GUI application.
        """
        
        #
        # Method should check the timer and should not work longer than
        # self._run_time_limit value.
        # start_time variable saves beginning time.
        #
        start_time = time()
        
        # 
        # You should call the base class "run" function to prepare common
        # stuff (e.g. fill the statistic information in stat record).
        #
        super(NewMethod, self).run(input_state, stat)
        
        # 
        # You should save some current things during the method's work
        # Among them: best found state, best found state's cost.
        # At each iteration you should send the ever found best state to the
        # main program via connection (self._connection).
        # Also the ever found best state should be returned by this method.
        # The cost of best found state should be stored in stat.solution_cost
        #

        #
        # In the code below @state and @value variables will save current state
        # and its value-cost. The state's value you can calculate with
        # cost function - self.calc_solution_cost
        # The @ever_found_best_state variables will contain the ever found best
        # state
        #
        ever_found_best_state = input_state.copy()
        state, value = input_state.copy(), self.calc_solution_cost(input_state)
        stat.solution_cost = value
        
        #
        # Below is a main loop that do all iterations.
        # It will run until the running time limit is reached.
        #
        while True:
            print '{:.2f}'.format(value)
            
            #
            # On each iteration you should send to the main program the 
            # current cost. Leave this code as it is.
            #
            self.send_current_cost(value, stat.solution_cost)
            
            #
            # On each iteration you should check the timer and if the function
            # works longer then self._run_time_limit return with failure.
            # Leave this code as it is.
            #
            if time()-start_time > self._run_time_limit:
                return ever_found_best_state, "Run time limit has been reached"
                
            #
            # Get the neighbor states for the current state using get_neighbors
            # function. This function calls BasicNeighborhood class' function
            # get_neighbors and returns a list of the neighbor states
            #
            new_states = self.get_neighbors(state)
            
            #
            # Now you should select a new state among the neighbors. This is an
            # essential point of your method and your overall search strategy.
            #
            # Here is an example of how the hill climbing method does this job.
            #
            #    best_state, best_value = None, float('inf')
            #    for new_state in new_states:
            #        v = self.calc_solution_cost(new_state)
            #        if v<best_value and v<value:
            #            best_state, best_value = new_state, v
            #    if not best_state:
            #        break
            #    state, value = best_state, best_value
            #
            
            #
            # On each iteration you should send to the main program a new
            # founded state and its cost. Leave this code as it is.
            #
            self.send_state(state, value)
            
            #
            # At the end of each iteration you should check if there is a new
            # best state. If so then you need save it and send to the main
            # application.
            #
            if value<stat.solution_cost:
                ever_found_best_state.copy_from(state)
                stat.solution_cost = value
                self.send_best_state(ever_found_best_state, value, stat)
            
            # 
            # At the end of each iteration you should collect memory and 
            # time statistics into statistic record.
            #
            stat.overall_nodes_generated += len(new_states)
            stat.overall_run_time = time() - start_time
            
        #
        # If we are running out of time then return the stored ever found
        # best state
        #
        return ever_found_best_state, "Local optimum is reached"