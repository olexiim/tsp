TSP Problem Solver is a software to solve travelling salesman problem using 
search paradigm. It provides GUI to display obtained solutions.
It allows users to add their own puzzles and methods for solving this TSP.

From Wikipedia:

    The travelling salesman problem (TSP) or travelling salesperson problem
    asks the following question: Given a list of cities and the distances 
    between each pair of cities, what is the shortest possible route that 
    visits each city exactly once and returns to the origin city? It is an 
    NP-hard problem in combinatorial optimization, important in operations 
    research and theoretical computer science.
    
    TSP can be modelled as an undirected weighted graph, such that cities are 
    the graph's vertices, paths are the graph's edges, and a path's distance 
    is the edge's length. It is a minimization problem starting and finishing 
    at a specified vertex after having visited each other vertex exactly once. 
    Often, the model is a complete graph (i.e. each pair of vertices is 
    connected by an edge). If no path exists between two cities, adding an 
    arbitrarily long edge will complete the graph without affecting the optimal 
    tour.

Tips of how to create your own search method.

    To create your own search method that solves the TSP problem you should 
    create a method class that inherited from the BasicMethod class 
    (methods/tsp/basicmethod.py). You should place a new method's file to the 
    folder of the problem (methods/tsp). When you finished creating your method 
    it will be accessible in the TSP Problem Solver main window. For more details 
    please refer a method template in methods/tsp/method_template.py file. 
    
Tips of how to create your own state neighborhoods.

    To create your own state neighborhoods that help to solve the problem you 
    should create a neighborhood class that inherited from the 
    BasicNeighborhood class (methods/neighborhood.py). You should place a new 
    neighborhood file to the folder of the problem (methods/tsp). Please 
    check methods/tsp/neighborhood.py for examples and exmplanations.

Project structure

    images - images folder
    methods - package for all methods
    methods/tsp - package of TSP problem methods
    methods/tsp/__init__.py - package init file (does nothing)
    methods/tsp/basicmethod.py - abstract method class for all methods for
                                    the N-queens problem
    methods/tsp/hill.py - module with Hill Climbing methods
    methods/tsp/method_template.py - module with description how to create 
                                        your own module
    methods/tsp/neighborhood.py - module with neighborhood strategies for
                                    the TSP problem
    methods/tsp/sa.py - module with Simulated annealing method
    methods/tsp/state.py - module with TspState class
    methods/tsp/tabu.py - module with Tabu method
    methods/__init__.py - package init file (does nothing)
    methods/method.py - module with most abstract method class called Method
    methods/neighborhood.py - module with BasicNeighborhood class
    methods/state.py - module with State class - abstract class for all other
                        problems' states
    methods/statrecord.py - module with StatRecord class
    main.py - main project module; run it to work with the TSP Problem Solver
    main_options.py - dialog window for main options of the Problem Solver
    main_options.ui - dialog window for main options QtDesigner
    main_window.py - main window module of the TSP Problem Solver
    main_window.ui - QtDesigner file for the main window
    tsp_board.py - module for envelope class for a TSP problem domain
    tsp_random_options.py - dialog window for the TSP problem random generating
    tsp_random_options.ui - dialog window for the TSP problem random generating 
                                    QtDesigner file
    
License agreement

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

Author information

    Oleksii Molchanovskyi
    National Technical University of Ukraine "Kyiv Polytechnic Institute"
    Kyiv, Ukraine
    E-mail: olexiim@gmail.com