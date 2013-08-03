#!/usr/bin/env python
"""Contains most abstract class for state implementation.

Contains class State that declares general functions for real states for a 
specific problem.

All other state classes should be iherited from this class.

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

class State(object):
    """Describes a state of a specific problem.
    
    Attributes:
        _state: some container (pure abstract)
    """
    _state = None
    
    def copy(self):
        """Copies current state object. Purely abstract.
        
        Returns:
            Copy of the object.
        """
        pass
        
    def __eq__(self, state):
        """Checks if the state is equal to this state object. Purely abstract.
        
        Args:
            state: 
        Returns:
            True if states are equal. False in other case.
        """
        pass
        
    def random_generate(self):
        """Generate a random state. Purely abstract.
        
        Returns:
            Randomly generated state.
        """
        pass
    
    def to_string(self):
        """Generate a string that describes this state. Purely abstract.
        
        Returns:
            A generated string for this state.
        """
        pass
    
    def __print__(self):
        """Prints this state. Runs to_string."""
        print self.to_string()