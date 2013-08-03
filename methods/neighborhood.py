#!/usr/bin/env python
"""Contains most abstract class for neighborhood implementation.

Contains class BasicNeighborhood that declares general functions for real 
neighborhoods.

All neighborhoods should be iherited from this class.

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

class BasicNeighborhood(object):
    """Base class for neighborhood.
    
    All other neighborhoods should be iherited from this class.
    
    Attributes:
        _name: heuristic title
        _short_name: shorter heuristic title
        _default: is this neighborhood would be default for a specific problem
            if there are several default neighborhoods the first one will be
            selected
        _disabled: is neighborhood dropped from the list of neighborhoods
    """
    
    _name = "Empty neighborhood"
    _short_name = "Empty"
    _default = False
    _disabled = False
    
    def get_neighbors(self, state):
        """Returns a list of neighbor states for the state. Returns empty list.
        
        Args:
            state:
            
        Returns:
            List of the states that are neighbors to the specified state.
        """
        return []
        
    def name(self):
        return self._name
        
    def short_name(self):
        return self._short_name
        
    def is_default(self):
        return self._default
        
    def is_disabled(self):
        return self._disabled