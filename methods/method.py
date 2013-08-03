#!/usr/bin/env python
"""Contains most abstract class for searching method implementation.

Contains class Method that declares general functions for the real methods. 
Also it implements some functions that a similar for all searching methods.

All methods should be inherited from the Method class.

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

from statrecord import StatRecord
from neighborhood import BasicNeighborhood

class Method(object):
    """Base class for search methods
    
    Attributes:
        _name: title of the method
        _short_name: shorter title 
        _type: method type (e.g. informed, local, etc.)
        _run_time_limit: amount of seconds that method can work
        _neighborhood: neighborhood object (used in get_neighbors function)
        _disabled: if True then method will not be active in GUI
        _connection: Pipe connection to send information packages to the
            main application
    """
    
    _name = "Basic method"
    _short_name = "Basic"
    _type = "Undefined"
    _run_time_limit = 60
    _neighborhood = None
    _disabled = False
    _connection = None
    
    def __init__(self, neighborhood=None, time_limit=None, args=None):
        """Inits the method object
        
        Args:
            heuristic: heuristic function object reference
            time_limit: time limit in seconds
            neighborhood: neighborhood objects list
            args: some additional argument that object can use
        """
        if not neighborhood:
            self._neighborhood = [BasicNeighborhood()]
        elif neighborhood.__class__.__name__=="list":
            self._neighborhood = neighborhood
        else:
            self._neighborhood = [neighborhood]
        if time_limit:
            self._run_time_limit = time_limit
        
    def name(self):
        """Returns method's name"""
        return self._name
        
    def short_name(self):
        """Returns method's short name"""
        return self._short_name
    
    def type(self):
        """Returns method's type"""
        return self._type
        
    def is_disabled(self):
        """Returns if the method is disabled"""
        return self._disabled
    
    def run(self, input_state, stat=StatRecord()):
        """Runs the method.
        
        Main function of the Method class. Runs the method.
        At this class it only stores static statistical information to a 
        statistic record.
        
        Args:
            input_state: initial state of the problem
            stat: object of type StatRecord that fill store all statistics
            
        Returns:
            Result of the method call in format [State, Message], where
            first parameter stores an ever found best state, while the 
            second parameter contains additional message in string format
            for GUI application.
        """
        stat.clear()
        stat.problem = "Unknown"
        stat.method = self._short_name
        if self._neighborhood:
            stat.neighborhood = ', '.join([x.short_name() for x in self._neighborhood])
        
    def get_neighbors(self, state):
        """Returns neighbors for the state.
        
        Get neighbors accordingly to self._heuristic object.
        
        Args:
            state: 
        
        Returns:
            List of states that a neighbors to the state.
        """
        neighbors = []
        for neighbohood in self._neighborhood:
            neighbors += neighbohood.get_neighbors(state)
        return neighbors
        
    def calc_solution_cost(self, state):
        """Calculates a state cost value. Returns zero."""
        return 0
        
    def set_connection(self, conn):
        """Stores pipe connection object"""
        self._connection = conn
        
    def send_current_cost(self, value, best_value=None):
        """Send cost value to the main application
        
        Args:
            value: cost value
            best_value: best cost value
        """
        if self._connection:
            try:
                self._connection.send(("cost",value,best_value))
            except:
                return
           
    def send_best_state(self, state, value, stat=None):
        """Send best state to the main application
        
        Args:
            state: state
            value: state's cost value
            stat: statistics record for this state
        """
        if self._connection:
            try:
                self._connection.send(("best_state", state, value, stat))
            except:
                return
           
    def send_state(self, state, value):
        """Send a state to the main application
        
        Args:
            state: state
            value: state's cost value
        """
        if self._connection:
            try:
                self._connection.send(("state", state, value))
            except:
                return