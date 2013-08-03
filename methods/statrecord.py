#!/usr/bin/env python
"""Contains class of the statistics record.

All methods of the TSP Problem Solver generate some statistic information 
during their work. Class StatRecord defines and stores this information. 
Its objects are used in method's run functions. 

Information that is stored in StatRecord will be shown in a statistics table
of the TSP Problem Solver GUI.

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

class StatRecord:
    """Stores statistics for each search method run
    
    Attributes:
        overall_nodes_generated: summarized amount of nodes (states) that were 
            generated during some method run
        overall_run_time: overall run time of a method
        problem: problem name
        method: method name (title)
        neighborhood: neighborhoods' names
        solution_cost: cost value of a solution of the problem
    """
    overall_run_time = 0
    problem = "Unknown"
    method = "Unknown"
    neighborhood = "Unknown"
    solution_cost = float('inf')
    overall_nodes_generated = 0
    
    def clear(self):
        self.overall_run_time = 0
        self.overall_nodes_generated = 0
        self.solution_cost = float('inf')
        self.problem = "Unknown"
        self.method = "Unknown"
        self.neighborhood = "Unknown"