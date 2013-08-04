#!/usr/bin/env python
"""Run script for TSP Problem Solver.

TSP Problem Solver is a software to solve travelling salesman problem using 
search paradigm. It provides GUI to display obtained solutions.
It allows users to add their own puzzles and methods for solving this TSP.

This is a main module for the TSP Problem Solver.

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

from main_window import Ui_MainWindow
from main_options import Ui_main_options
from tsp_random_options import Ui_tsp_random_options

from tsp_board import TspBoard

from methods.statrecord import StatRecord
from methods.tsp.state import TspState

import sys
import inspect
import time
import os
from os.path import isfile, join, split
from importlib import import_module
from multiprocessing import Process, Pipe
from numpy import average
from PyQt4 import QtCore, QtGui

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class AsyncRunProcess(Process):
    """Class that implements methods running in a separate process"""
        
    def __init__(self, obj, state, conn):
        Process.__init__(self)
        self.obj = obj
        self.state = state.copy()
        self.conn = conn
#        print "Calculation process initialized"
    def run(self):
        stat = StatRecord()
        self.obj.set_connection(self.conn)
        result_state, msg = self.obj.run(self.state, stat)
#        print result_state.to_string(), msg, self.state._state
        self.conn.send(("finish",result_state, msg, stat))
#        self.conn.close()
        
class AsyncRun(QtCore.QObject):
    """Class that runs method instance for a problem asynchronously"""
    stop = False
    def __init__(self, obj, state, options={}):
        QtCore.QObject.__init__(self)
        self.obj = obj
        self.state = state
        self.options = options
        if not self.options.has_key('runtime_cost'):
            self.options['runtime_cost'] = False
        if not self.options.has_key('runtime_state'):
            self.options['runtime_state'] = False
        if not self.options.has_key('cost_avg_num'):
            self.options['cost_avg_num'] = 10
        if not self.options.has_key('runtime_best_state'):
            self.options['runtime_best_state'] = False
        
    def run(self):
        print self.obj.name() + " starts"
        
        parent_conn, child_conn = Pipe()
        stat = StatRecord()
        self.process = AsyncRunProcess(self.obj, self.state, child_conn)
#        print "Starting calculation process..."
        self.process.start()
        av_cost, av_cost_len, best_cost = [], 0, float('inf')
        best_solution_value, best_state, best_stat = float('inf'), self.state.copy(), StatRecord()
        while not self.stop:
            if parent_conn.poll():
                while parent_conn.poll() and not self.stop:
                    msg = parent_conn.recv()
                    if msg[0]=="cost" and self.options['runtime_cost']:
#                        print msg[1]
                        av_cost_len += 1
                        av_cost.append(msg[1])
                        if msg[2]:
                            b_cost = msg[2]
                            if b_cost<best_cost:
                                best_cost = b_cost
                        if av_cost_len==self.options['cost_avg_num']:
                            self.emit(QtCore.SIGNAL("display_value"), average(av_cost), best_cost)
                            av_cost, av_cost_len = [], 0
                            time.sleep(0.01)
                    if msg[0]=="state" and self.options['runtime_state']:
                        state, value = msg[1:]
#                        if :
#                            if best_solution_value>value:
#                                best_solution_value = value
#                                self.emit(QtCore.SIGNAL("display_state"), state, value)
#                                time.sleep(0.01)
#                        else:
                        self.emit(QtCore.SIGNAL("display_state"), state, value)
                        time.sleep(0.01)
                    if msg[0]=="best_state":
                        best_state, best_solution_value, best_stat = msg[1:]
                        if self.options['runtime_best_state']:
                            self.emit(QtCore.SIGNAL("display_state"), best_state, best_solution_value)
                            time.sleep(0.01)
                    if msg[0]=="finish":
                        state, msg, stat = msg[1:]
                        print "Calculation finished"
#                        print msg, state.to_string()
                        self.process.join()
                        self.emit(QtCore.SIGNAL("success"), state, msg, stat)
                        time.sleep(1)
                        self.emit(QtCore.SIGNAL("finished"))
                        return
            else:
                time.sleep(0.1)
        if self.stop:
            print "Stop the run object"#, best_state.to_string()
            self.emit(QtCore.SIGNAL("success"), best_state, "Stopped on demand", best_stat)
            time.sleep(1)
            self.process.terminate()
            self.process.join()
#        elif parent_conn.poll():
#            state, msg, stat = parent_conn.recv()
#            print "Calculation finished"
#            print msg, state.to_string()
#            self.process.join()
#            self.emit(QtCore.SIGNAL("success"), state, msg, stat)
        self.emit(QtCore.SIGNAL("finished"))
    
    def stopWork(self):
        print "Calculation terminated"
        self.stop = True

class MainOptionsDlg(QtGui.QDialog):
    """Envelope-class for main options dialog"""
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_main_options()
        self.ui.setupUi(self)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.runtime_chart.stateChanged.connect(self.runtime_chart_changed)
        
    def runtime_chart_changed(self, index):
        self.ui.avg_solution.setEnabled(index==QtCore.Qt.Checked)
        self.ui.avg_solution_label.setEnabled(index==QtCore.Qt.Checked)
        
class TSPRandomOptionsDlg(QtGui.QDialog):
    """Envelope-class for TSP random generating dialog"""
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_tsp_random_options()
        self.ui.setupUi(self)
        self.ui.cities_num.setFocus()
        self.ui.cities_num.selectAll()
        
class MainWindow(QtGui.QMainWindow):
    """Main TSP Problem SOlver class.
    
    Shows the main window and runs methods for the problems.
    
    Attributes:
        _method_path: path to methods module
        _method_modules: list of loaded methods for a current problem
        _method_types: list of loaded method types
        _neighborhoods: list of loaded heighborhood modules
        _current_state: current state
        _original_state: starting state
        _current_problem: current problem shortcut
        _current_problem_title: current problem title
        _current_problem_short_title: current problem short title
        _board_scene: object of QGraphicsScene, used to display a board
        _board_scene_removable: a list of objects that a dynamic on a board
        _board_data: data used to display board
        _statistics: list of all statistic records
        _run_queue: queue of problem tasks
        _has_solution: flag to know if there solution was found
        _is_displaying_runtime: 
        _is_displaying_runtime_state:
        main_options: GUI options of the Problem Solver
        _chart_max_value: maximum height (cost value) of chart data
        _chart_min_value: minimum height (cost value) of chart data
        _chart_prev_value: previous value on a dynamic chart
        _chart_prev_best_value: currently best cost value
        tsp_cities_num: number of cities in TSP problem
        tsp_filename: TSP file name
        tsp_board: TspBoard object
        run_thread: object of a thread that runs a searching method
        run_object: object of class AsyncRun
    """
    
    _method_path = 'methods'
    _method_modules = {}
    _method_types = []
    _neighborhoods = {}
    _current_state = None
    _original_state = None
    _current_problem = ''
    _current_problem_title = ''
    _current_problem_short_title = ''
    
    _board_scene = None
    _board_scene_removable = []
    _board_data = None
    
    _statistics = []
    _run_queue = []
    _has_solution = False
    _is_displaying_runtime = False
    _is_displaying_runtime_state = False
    
    main_options = {'runtime_chart':True, 'runtime_solution':False, 
                    'avg_solution':1, 'runtime_best':False}
    
    _chart_max_value = 0
    _chart_min_value = float('inf')
    _chart_prev_value = None
    _chart_prev_best_value = float('inf')
    
    # problem parameteres
    # TSP
    tsp_cities_num = 4
    tsp_filename = ""
    tsp_board = TspBoard()
    
    run_thread = None
    run_object = None
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.disable_methods()
        self.clear_board()
        
        # init run button menu
        self.run_menu = QtGui.QMenu()
        self.run_menu.addAction("Run once", self.run_once)
        self.run_menu.addAction("Run checked methods", self.run_checked_methods)
        self.run_menu.addAction("Run all methods", self.run_all_variants)
        self.ui.run.setMenu(self.run_menu)
        
        # status bar
        self.timer_widget = QtGui.QLabel()
        self.run_timer = QtCore.QTimer(self)
        self.run_timer.timeout.connect(self.update_timer)
        
        # init stat table
        header_labels = ["##","Problem","Method","Neighborhood",
                "Solution cost","Time, sec", "Overall states"]
        self.ui.stat_table.setHorizontalHeaderLabels(header_labels)
        self.ui.stat_table.resizeColumnsToContents() # autoresize based on header text width
        self.ui.stat_table.setColumnWidth(1, 110) # extend Problem header width
        self.ui.stat_table.setColumnWidth(2, 120) # extend Problem header width
        self.ui.stat_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ui.stat_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        
        QtCore.QObject.connect(self.ui.run,QtCore.SIGNAL("clicked()"), self.run_once)
        
        self.ui.actionGenerate_new.triggered.connect(self.new_random)
        self.ui.actionLoad_from_file.triggered.connect(self.new_load)
        self.ui.actionSave.triggered.connect(self.save_problem)
        self.ui.actionRestart.triggered.connect(self.restart)
        self.ui.actionRun_once.triggered.connect(self.run_once)
        self.ui.actionRun_checked_methods.triggered.connect(self.run_checked_methods)
        self.ui.actionRun_all_methods.triggered.connect(self.run_all_variants)
        self.ui.actionStop.triggered.connect(self.stop)
        self.ui.actionClear.triggered.connect(self.clear_statistics)
        self.ui.actionDelete_selected.triggered.connect(self.delete_selected_statistics)
        self.ui.actionImportTo_CSV.triggered.connect(self.import_to_csv)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionOptions.triggered.connect(self.popup_main_options_dlg)
        
        self.ui.methods_tree.itemDoubleClicked.connect(self.methods_tree_item_clicked)
        self.ui.stat_table.currentItemChanged.connect(self.stat_table_item_changed)
        self.ui.main_splitter.splitterMoved.connect(self.process_resize)
        self.ui.splitter_2.splitterMoved.connect(self.process_resize)
        
        self.ui.stat_table.keyPressEvent = self.process_statistics_keys_event
        
        self.ui.tab_widget.setCurrentIndex(0)

    def process_resize(self, event):
        """Processes a window resize event"""
        sr = self.ui.runtime_chart.sceneRect()
        g = self.ui.runtime_chart_frame.geometry()
        if sr.width()>g.width():
            self.ui.runtime_chart.setGeometry(g.width()-sr.width(), 0, sr.width(), g.height())
        else:
            self.ui.runtime_chart.setGeometry(0, 0, sr.width(), g.height())
        self.ui.runtime_chart.fitInView(sr, QtCore.Qt.IgnoreAspectRatio)
        self.ui.board.fitInView(self.ui.board.sceneRect(), QtCore.Qt.KeepAspectRatio)
    
    def resizeEvent(self, event):
        """Slot that processes a window resize event"""
        QtGui.QWidget.resizeEvent(self, event)
        self.process_resize(event)
        
    def popup_main_options_dlg(self):
        """Pop-ups a main options dialog"""
        dialog = MainOptionsDlg(self)
        dialog.ui.runtime_chart.setCheckState(self.main_options['runtime_chart'] and QtCore.Qt.Checked or QtCore.Qt.Unchecked)
        dialog.ui.runtime_solution.setCheckState(self.main_options['runtime_solution'] and QtCore.Qt.Checked or QtCore.Qt.Unchecked)
        dialog.ui.runtime_best.setCheckState(self.main_options['runtime_best'] and QtCore.Qt.Checked or QtCore.Qt.Unchecked)
        dialog.ui.avg_solution.setValue(self.main_options['avg_solution'])
        dialog.ui.avg_solution.setEnabled(self.main_options['runtime_chart'])
        dialog.ui.avg_solution_label.setEnabled(self.main_options['runtime_chart'])
        if dialog.exec_():
            self.main_options['runtime_chart'] = dialog.ui.runtime_chart.checkState()==QtCore.Qt.Checked
            self.main_options['runtime_solution'] = dialog.ui.runtime_solution.checkState()==QtCore.Qt.Checked
            self.main_options['runtime_best'] = dialog.ui.runtime_best.checkState()==QtCore.Qt.Checked
            self.main_options['avg_solution'] = dialog.ui.avg_solution.value()
            self.ui.tab_widget.setTabEnabled(1, self.main_options['runtime_chart'])
            return True
        return False
    
    def clear_method_lists(self):
        """Delete all methods from the interface lists"""
        self.ui.methods_tree.clear()
        self.ui.neighborhood_list.clear()
        
    def disable_methods(self):
        """Disables methods list"""
        self.ui.run_groupbox.setEnabled(False)
    
    def update_method_lists(self, reload_modules=True):
        """Loads methods, heuristics, and neighborhoods
        
        Args:
            reload_modules
        """
        
        def is_subclass(class_obj, parent_class_name, strictly=True):
            if strictly and class_obj.__name__==parent_class_name:
                return False
            for cl in inspect.getmro(class_obj):
                if cl.__name__==parent_class_name:
                    return True
            return False
            
        self.ui.run_groupbox.setEnabled(True)
            
        if reload_modules:
            self.clear_method_lists()
            
            self.ui.methods_tree.addTopLevelItem(QtGui.QTreeWidgetItem(['Methods']))
            root = self.ui.methods_tree.topLevelItem(0)
            root.setFlags(root.flags().__or__(QtCore.Qt.ItemIsTristate))
            root.setCheckState(0, QtCore.Qt.Unchecked)
            root.setExpanded(True)
            self._method_types = []
            
            method_path = self._method_path + os.sep + self._current_problem
            method_files = [ f for f in os.listdir(method_path) if isfile(join(method_path,f)) and f.endswith('.py') ]
            sys.path.append(join(sys.path[0], method_path))
            
            self._method_modules = {}
            self._neighborhoods = {}
            for method_file in method_files:
                module_name = 'methods.'+self._current_problem+'.'+method_file.replace('.py','')
                import_module(module_name)
                for name, obj in inspect.getmembers(sys.modules[module_name]):
                    # method
                    if inspect.isclass(obj) and is_subclass(obj,"BasicMethod"):
                        if not obj._type in self._method_types:
                            self._method_types.append(obj._type)
                            root.addChild(QtGui.QTreeWidgetItem([obj._type]))
                            child = root.child(root.childCount()-1)
                            child.setCheckState(0, QtCore.Qt.Unchecked)
                            child.setExpanded(True)
                            font = child.font(0)
                            font.setBold(True)
                            child.setFont(0, font)
                            child.setFlags(root.flags().__or__(QtCore.Qt.ItemIsTristate))
                        
                        if not obj._disabled:
                            self._method_modules[obj.__name__] = {'file':method_file, 'type':obj._type, 'class':obj, 'title':obj._name, 'short_title':obj._short_name, 'module':module_name}
                        parent = self.ui.methods_tree.findItems(obj._type, QtCore.Qt.MatchFlags(QtCore.Qt.MatchFixedString + QtCore.Qt.MatchRecursive))
                        if parent:
                            parent = parent[0]
                            parent.addChild(QtGui.QTreeWidgetItem([obj._name]))
                            child = parent.child(parent.childCount()-1)
                            child.setCheckState(0, QtCore.Qt.Unchecked)
                            child.setData(1, QtCore.Qt.UserRole, obj.__name__)
                            if obj._disabled:
                                child.setDisabled(True)

                    # neighborhood
                    if inspect.isclass(obj) and is_subclass(obj,"BasicNeighborhood") and not obj._disabled:
                        self._neighborhoods[obj.__name__] = {'file':method_file, 'module':module_name, 'class':obj, 'title':obj._name, 'short_title':obj._short_name}
                        self.ui.neighborhood_list.addItem(obj._name)
                        item = self.ui.neighborhood_list.item(self.ui.neighborhood_list.count()-1)
                        item.setData(QtCore.Qt.UserRole, obj.__name__)
                        if obj._default:
                            item.setCheckState(QtCore.Qt.Checked)
                        else:
                            item.setCheckState(QtCore.Qt.Unchecked)
    
    def popup_tsp_random_options_dlg(self):
        """Pop-ups a TSP options dialog"""
        dialog = TSPRandomOptionsDlg(self)
        dialog.ui.cities_num.setValue(self.tsp_cities_num)
        dialog.ui.cities_num.selectAll()
        if dialog.exec_():
            self.tsp_cities_num = dialog.ui.cities_num.value()
            return True
        return False
        
    def enable_window_items(self, enable=True):
        """Enables or disables interface elements before/after method's run"""
        enable_objects = [self.ui.methods_tree, self.ui.neighborhood_list, self.ui.time_limit,
                          self.ui.actionRun_once, self.ui.actionRun_checked_methods, 
                          self.ui.actionRun_all_methods, self.ui.menuProblem]
        if enable:
#            self.ui.methods_tree.setEnabled(True)
#            self.ui.neighborhood_list.setEnabled(True)
#            self.ui.time_limit.setEnabled(True)
            self.ui.run.setText("Run")
            self.run_menu.setEnabled(True)
            self.ui.actionStop.setEnabled(False)
            for obj in enable_objects:
                obj.setEnabled(True)
            
        else:
#            self.ui.methods_tree.setEnabled(False)
#            self.ui.neighborhood_list.setEnabled(False)
#            self.ui.time_limit.setEnabled(False)
            self.ui.run.setText("Stop")
            self.run_menu.setEnabled(False)
            self.ui.actionStop.setEnabled(True)
            for obj in enable_objects:
                obj.setEnabled(False)
                
    def before_run(self, problem_title="", method_title=""):
        """Function that runs before a solving method
        
        Args:
            problem_title: 
            method_title:
        """
        msg = 'Run'
        if problem_title:
            msg += ' ' + problem_title
        if method_title:
            msg += ' with ' + method_title + ' method'

        self.ui.statusbar.showMessage(msg)
        self.elapsed_timer = QtCore.QElapsedTimer()
        self.elapsed_timer.start()
        self.run_timer.start(1000)
        self.ui.statusbar.addPermanentWidget(self.timer_widget)
        self.timer_widget.show()
        self.timer_widget.setText('00:00')
#        self.erase_runtime_chart()
        if self.main_options['runtime_chart']:
            self.ui.tab_widget.setCurrentIndex(1)
        else:
            self.ui.tab_widget.setCurrentIndex(0)
        
#        self.ui.board.setForegroundBrush(QtGui.QBrush(QtCore.Qt.lightGray,QtCore.Qt.Dense6Pattern))
        self.ui.board.setForegroundBrush(QtGui.QBrush(QtGui.QColor(235,233,237,127)))
        self.ui.board.repaint()
        self.enable_window_items(enable=False)
    
    def after_run(self, result_state=None, msg="", stat=StatRecord()):
        """Function that runs after a solving method
        
        Args:
            result_state: found state
            msg: string that will be displayed in a status bar
            stat: statistics, type StatRecord
        """
        if result_state:
            print "After run", result_state.to_string(), msg
        else:
            print "After run with no params"
        self.run_thread.wait()
        del self.run_thread
        self.run_thread = None
        del self.run_object
        self.run_object = None
    
        self.run_timer.stop()
        del self.elapsed_timer
        self.ui.statusbar.removeWidget(self.timer_widget)
        self.ui.statusbar.showMessage(msg, 1000*60)
        
        if result_state:
            self._has_solution = True
            self._current_state = result_state.copy()
            self.display_board(self._current_state)
            self.add_statistics(stat, result_state.copy())
        
        if self._run_queue:
            time.sleep(1)
        if self.process_run_queue():
            return
        
        self.ui.board.setForegroundBrush(QtGui.QBrush(QtCore.Qt.lightGray,QtCore.Qt.NoBrush))
        self.ui.board.repaint()
        self.ui.tab_widget.setCurrentIndex(0)
        self.enable_window_items()
        
    def _process_new_tsp_problem(self, problem_title, problem_short_title):
        """Runs after new problem is randomly created or loaded
        
        Args:
            problem_title: 
            problem_short_title:
        """
        self._original_state = TspState(self.tsp_board.cities_num())
        self._current_state = self._original_state
        self._current_problem = "tsp"
        self._current_problem_title = problem_title
        self._current_problem_short_title = problem_short_title
        self._has_solution = False
        self._board_scene = None
        self.display_board(self._current_state)
        self.ui.actionRestart.setEnabled(True)
        self.ui.actionSave.setEnabled(True)
        self.erase_runtime_chart()
    
    def new_random(self):
        """Process a menu action "Problem/Generate new..."""
        prev_problem = self._current_problem
#        selected_problem = self.ui.problem_list.itemData(self.ui.problem_list.currentIndex()).toString().__str__()
        selected_problem = "tsp"
        if selected_problem=="tsp":
            if self.popup_tsp_random_options_dlg():
                self.tsp_board.random(self.tsp_cities_num)
                self._process_new_tsp_problem("Random TSP with %d cities" % (self.tsp_cities_num,), "TSP %d cities" % (self.tsp_cities_num,))
        if prev_problem!=self._current_problem:
            self.update_method_lists()
            self.clear_statistics()
            
    def new_load(self):
        """Process a menu action "Problem/Load from file..."""
        prev_problem = self._current_problem
        selected_problem = "tsp"
        
        open_dlg = QtGui.QFileDialog(self, "Load problem", ".")
        open_dlg.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        open_dlg.setFileMode(QtGui.QFileDialog.ExistingFile)
        if selected_problem=="tsp":
            open_dlg.setDefaultSuffix("tsp")
            open_dlg.setNameFilters(["TSP files (*.tsp)","Any files (*)"])
        if open_dlg.exec_():
            file_name = open_dlg.selectedFiles()[0].__str__()
            if not file_name:
                return
            if selected_problem=="tsp":
                self.tsp_board.load_from_file(file_name)
                self.tsp_cities_num = self.tsp_board.cities_num()
                self._process_new_tsp_problem("TSP with %d cities (%s)" % (self.tsp_cities_num, split(file_name)[1]), "TSP %d cities (%s)" % (self.tsp_cities_num, split(file_name)[1]))
        if prev_problem!=self._current_problem:
            self.update_method_lists()
            self.clear_statistics()
    
    def save_problem(self):
        """Process a menu action "Problem/Save..."""
        save_dlg = QtGui.QFileDialog(self, "Save problem", ".")
        save_dlg.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        if self._current_problem=="tsp":
            save_dlg.setDefaultSuffix("tsp")
            save_dlg.setNameFilters(["TSP files (*.tsp)","Any files (*)"])
        if save_dlg.exec_():
            file_name = save_dlg.selectedFiles()[0].__str__()
            if not file_name:
                return
            if self._current_problem=="tsp":
                self.tsp_board.save_to_file(file_name)
    
    def restart(self):
        """Process a menu action "Run/Restart..."""
        self._current_state = self._original_state.copy()
        self._current_state.randomize()
        self._has_solution = False
        self._board_scene = None
        self.display_board(self._current_state)
        self.erase_runtime_chart()
    
    def display_board(self, state=None, board=None, has_solution=False, use_board_scene=True):
        """Displays the Problem Solver board for a state
        
        Args:
            state: state to disaply on board; if not defined, then takes 
                current state
            board: 
            has_solution: 
            use_board_scene:
        """
        if not state:
            state = self._current_state
        if not state:
            self.clear_board()
        if self._current_problem=="tsp":
            if not board:
                board = self.tsp_board
            self.display_board_tsp(state, board, has_solution, use_board_scene)
        else:
            self.clear_board()
    
    def display_board_tsp(self, state, board=None, has_solution=False, use_board_scene=True):
        """Displays TSP board for a state
        
        Args:
            state: state to disaply on board; if not defined, then takes 
                current state
            board: 
            has_solution: 
            use_board_scene:
        """
        new_board = False
        if not self._board_scene and use_board_scene:
            self._board_scene = QtGui.QGraphicsScene()
            self._board_scene_removable = []
            scene = self._board_scene
            new_board = True
        elif not use_board_scene:
            scene = QtGui.QGraphicsScene()
            new_board = True
        
#        scene = QtGui.QGraphicsScene()
        cities = []
        if new_board:
            board_width = board_height = min(board.max_x()-board.min_x(), board.max_y()-board.min_y())
            city_width = city_height = max(board_width*0.01, 4)

            scene.setSceneRect(0,0,board_width,board_height)
#            scene.addRect(0,0,board_width,board_height, QtGui.QPen(QtCore.Qt.white), QtGui.QBrush(QtCore.Qt.white))
            x_coef = float(board_width*0.9) / (board.max_x() - board.min_x())
            y_coef = float(board_height*0.9) / (board.max_y() - board.min_y())
            x_delta, y_delta = board_width*0.05, board_height*0.05
            if x_coef<y_coef:
                y_coef = x_coef
            elif y_coef<x_coef:
                x_coef = y_coef
                
            for city in board.cities():
                cities.append(((city[0]-board.min_x())*x_coef+x_delta, 
                               (city[1]-board.min_y())*y_coef+y_delta))
            for i in range(len(cities)):
                scene.addRect(cities[i][0]-city_width/2, cities[i][1]-city_height/2, city_width, city_height, QtGui.QPen(QtCore.Qt.black), QtGui.QBrush(QtCore.Qt.black))
            
            if use_board_scene:
                scene = self._board_scene
                self._board_data = cities
        elif not new_board and use_board_scene:
            scene = self._board_scene
            cities = self._board_data
            if self._board_scene_removable:
                for item in self._board_scene_removable:
                    scene.removeItem(item)
            
        if self._has_solution or has_solution:
            if use_board_scene:
                self._board_scene_removable = []
            prev_city = state._cities[state.cities_num()-1]
            for next_city in state._cities:
                new_item = scene.addLine(cities[prev_city][0], cities[prev_city][1], cities[next_city][0], cities[next_city][1], QtGui.QPen(QtCore.Qt.black))
                if use_board_scene:
                    self._board_scene_removable.append(new_item)
                prev_city = next_city
        self.ui.board.setScene(scene)
        self.ui.board.fitInView(scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        return True
        
    def clear_board(self):
        """Clears a board"""
        scene = QtGui.QGraphicsScene()
        self.ui.board.setScene(scene)
        self._board_scene = None
        
    def stop(self):
        """Stops method running"""
        if self.run_thread:
#            print "Begin termination..."
            self._run_queue = []
#            print "Run after_run"
#            self.after_run()
            self.run_object.emit(QtCore.SIGNAL("finished"))
#            print "After run completed"
    
    def process_run_queue(self):
        """Process a queue of the problem tasks"""
        if not self._run_queue:
            return False
            
        method, neighborhood, self._current_state = self._run_queue.pop(0)
        print 'Next task:', self._current_problem, method
        self.before_run(problem_title=self._current_problem_title, method_title=self._method_modules[method]['title'])
        self.async_run(method, neighborhood)
        return True
    
    def run_once(self):
        """Runs currently selected method for the problem"""
        if self.run_thread:
            return self.stop()
            
        items = self.ui.methods_tree.selectedItems()
        if not items:
            self.show_message("No method selected")
            return
        method = items[0].data(1, QtCore.Qt.UserRole).toString().__str__()

        neighborhood = self.get_checked_neighborhoods()
        if not neighborhood:
            self.show_message("Please select a method")
            return
        
        if self._method_modules.has_key(method):
            self._run_queue.append((method, neighborhood, self._current_state.copy()))
            self.process_run_queue()
    
    def run_checked_methods(self):
        """Runs checked methods for the problem"""
        if self.run_thread:
            return self.stop()
            
        methods = self.get_checked_methods()
        neighborhood = self.get_checked_neighborhoods()
        if not neighborhood:
            self.show_message("No neighborhood selected")
            return
        
        for method in methods:
            if self._method_modules.has_key(method):
                self._run_queue.append((method, neighborhood, self._current_state.copy()))
        self.process_run_queue()
    
    def run_all_variants(self):
        """Runs all possible variants of methods"""
        if self.run_thread:
            return self.stop()
        
        neighborhood = self.get_checked_neighborhoods()
        if not neighborhood:
            self.show_message("No neighborhood selected")
            return
        
        methods = self.get_checked_methods(only_checked=False)
        for method in methods:
            if self._method_modules.has_key(method):
                self._run_queue.append((method, neighborhood, self._current_state.copy()))
        self.process_run_queue()
            
    def async_run(self, method, neighborhoods):
        """Makes an asynchronous run of the method

        Args:
            method: name of the method to run
            neighborhoods: list of the neighborhood's names
        """
        neighborhood_classes = []
        for neighborhood in neighborhoods:
            neighborhood_classes.append(self._neighborhoods[neighborhood]['class']())
        obj = self._method_modules[method]['class'](neighborhood=neighborhood_classes, time_limit=self.ui.time_limit.value(), args=self.get_problem_args())
        run_options = {'runtime_cost': self.main_options['runtime_chart'],
                       'runtime_state': self.main_options['runtime_solution'],
                       'cost_avg_num': self.main_options['avg_solution'],
                       'runtime_best_state': self.main_options['runtime_best']}
        self.run_object = AsyncRun(obj, self._current_state, run_options)
        self.run_thread = QtCore.QThread()
        QtCore.QObject.connect(self.run_thread, QtCore.SIGNAL("started()"), self.run_object.run, QtCore.Qt.DirectConnection);
        QtCore.QObject.connect(self.run_thread, QtCore.SIGNAL("finished()"), self.run_object.deleteLater, QtCore.Qt.DirectConnection);
        QtCore.QObject.connect(self.run_object, QtCore.SIGNAL("finished"), self.run_object.stopWork, QtCore.Qt.DirectConnection);
        QtCore.QObject.connect(self.run_object, QtCore.SIGNAL("finished"), self.run_object.deleteLater, QtCore.Qt.DirectConnection);
        QtCore.QObject.connect(self.run_object, QtCore.SIGNAL("finished"), self.run_thread.quit, QtCore.Qt.DirectConnection);
        QtCore.QObject.connect(self.run_object, QtCore.SIGNAL("success"), self.after_run)

        QtCore.QObject.connect(self.run_object, QtCore.SIGNAL("display_value"), self.display_runtime_chart)
        QtCore.QObject.connect(self.run_object, QtCore.SIGNAL("display_state"), self.display_runtime_state)
        self.run_object.moveToThread(self.run_thread)
        self.run_thread.start()
        
    def methods_tree_item_clicked(self):
        """Slot for clicking on method signal"""
        if not self.run_thread:
            self.run_once()
            
    def get_checked_methods(self, only_checked=True):
        """Returns all checked methods in the tree
        
        Args:
            only_checked:
        
        Returns:
            A list of names of checked methods
        """
        def process_node(node, level, check_list):
            if node.childCount()==0 and level>=3 and (node.checkState(0)==QtCore.Qt.Checked or not only_checked):
                check_list.append(node.data(1, QtCore.Qt.UserRole).toString().__str__())
            for c in range(node.childCount()):
                process_node(node.child(c), level+1, check_list)
        
        root = self.ui.methods_tree.topLevelItem(0)
        check_list = []
        process_node(root, 1, check_list)
        return check_list
        
    def get_checked_neighborhoods(self, only_checked=True):
        """Returns all checked neighborhoods in the neighborhood list
        
        Args:
            only_checked:
        
        Returns:
            A list of names of checked neighborhoods
        """
        check_list = []
        for i in range(self.ui.neighborhood_list.count()):
            item = self.ui.neighborhood_list.item(i)
            if item.checkState()==QtCore.Qt.Checked or not only_checked:
                check_list.append(item.data(QtCore.Qt.UserRole).toString().__str__())
        return check_list
        
    def get_problem_args(self):
        if self._current_problem=="tsp":
            return [self.tsp_board.distance_matrix()]
        return None
        
    """
    Statistics stuff
    """
    
    def enable_statistics_actions(self, enable=True):
        """Enables or disables statistics table during method run
        
        Args:
            enable: True/False
        """
        self.ui.actionSave_history.setEnabled(enable)
        self.ui.menuImport.setEnabled(enable)
        self.ui.actionClear.setEnabled(enable)
        self.ui.actionDelete_selected.setEnabled(enable)
    
    def add_statistics(self, stat=StatRecord(), state=None):
        """Adds a statistic record to the statistics table.
        
        Args:
            stat: statistic object, type: StatRecord
            state: state
        """
        if not stat:
            return
        print "Adding statistics..."
        self._statistics.append({'statistics':stat, 'state':state, 'board':self.tsp_board.copy(), 'problem':self._current_problem})
        row = self.ui.stat_table.rowCount()
        self.ui.stat_table.insertRow(row)
        self.ui.stat_table.setItem(row, 0, QtGui.QTableWidgetItem(str(row+1)))
        self.ui.stat_table.setItem(row, 1, QtGui.QTableWidgetItem(self._current_problem_short_title))
        self.ui.stat_table.setItem(row, 2, QtGui.QTableWidgetItem(stat.method))
        self.ui.stat_table.setItem(row, 3, QtGui.QTableWidgetItem(stat.neighborhood))
        self.ui.stat_table.setItem(row, 4, QtGui.QTableWidgetItem('{:,.2f}'.format(stat.solution_cost)))
        self.ui.stat_table.item(row,4).setTextAlignment(QtCore.Qt.AlignRight+QtCore.Qt.AlignVCenter)
        self.ui.stat_table.setItem(row, 5, QtGui.QTableWidgetItem("%.3f"%stat.overall_run_time))
        self.ui.stat_table.item(row,5).setTextAlignment(QtCore.Qt.AlignRight+QtCore.Qt.AlignVCenter)
        self.ui.stat_table.setItem(row, 5, QtGui.QTableWidgetItem("%.3f"%stat.overall_run_time))
        self.ui.stat_table.setItem(row, 6, QtGui.QTableWidgetItem('{:,d}'.format(stat.overall_nodes_generated)))
        self.ui.stat_table.item(row,6).setTextAlignment(QtCore.Qt.AlignRight+QtCore.Qt.AlignVCenter)
        self.ui.stat_table.item(row,1).setData(QtCore.Qt.UserRole, len(self._statistics)-1)
        self.ui.stat_table.resizeRowsToContents()
        self.ui.stat_table.scrollToItem(self.ui.stat_table.item(row,0))
        
        self.enable_statistics_actions()
        
    def stat_table_item_changed(self):
        """Slot that handles changes of the statistic record in the list"""
        if self.ui.stat_table.isEnabled():
            if self.ui.stat_table.rowCount():
                state_num = self.ui.stat_table.item(self.ui.stat_table.currentRow(),1).data(QtCore.Qt.UserRole).toInt()[0]
                self.display_board(self._statistics[state_num]['state'], self._statistics[state_num]['board'], has_solution=True, use_board_scene=False)
    
    def clear_statistics(self):
        """Clears statistics"""
        self.ui.stat_table.setDisabled(True)
        for row in range(self.ui.stat_table.rowCount()):
            self.ui.stat_table.removeRow(0)
        self.ui.stat_table.setEnabled(True)
        self.enable_statistics_actions(False)
        
    def delete_selected_statistics(self):
        """Delete selected statistic records"""
        self.ui.stat_table.setDisabled(True)
        ranges = self.ui.stat_table.selectedRanges()
        rows = []
        for range_ in ranges:
            for r in range(range_.topRow(), range_.bottomRow()+1):
                rows.append(r)
        rows.sort(reverse = True)
        for row in rows:
            self.ui.stat_table.removeRow(row)
        for row in range(self.ui.stat_table.rowCount()):
            self.ui.stat_table.setItem(row, 0, QtGui.QTableWidgetItem(str(row+1)))
        self.ui.stat_table.setEnabled(True)
        if self.ui.stat_table.rowCount()==0:
            self.enable_statistics_actions(False)
            
    def process_statistics_keys_event(self, event):
        """Process key clicks for statistics table"""
        QtGui.QTableWidget.keyPressEvent(self.ui.stat_table, event)
        if event.key()==QtCore.Qt.Key_Delete and self.ui.stat_table.currentRow()>=0:
            self.ui.stat_table.setDisabled(True)
            row = self.ui.stat_table.currentRow()
            self.ui.stat_table.removeRow(row)
            for r in range(row, self.ui.stat_table.rowCount()):
                self.ui.stat_table.setItem(r, 0, QtGui.QTableWidgetItem(str(r+1)))
            self.ui.stat_table.setEnabled(True)
            if self.ui.stat_table.rowCount()==0:
                self.enable_statistics_actions(False)
            
    def import_to_csv(self):
        """Imports all statistic records to CSV-format file"""
        save_dlg = QtGui.QFileDialog(self, "Import history", ".")
        save_dlg.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        save_dlg.setDefaultSuffix("csv")
        save_dlg.setNameFilters(["CSV files (*.csv)","Any files (*)"])
        if save_dlg.exec_():
            file_name = save_dlg.selectedFiles()[0].__str__()
            if not file_name:
                return
#        filename = 'import.csv'
            col_count = self.ui.stat_table.columnCount()
            with open(file_name, 'w') as f:
                header = [self.ui.stat_table.horizontalHeaderItem(col).text().__str__() for col in range(col_count)] + ["State"]
                f.write(";".join(header))
                for row in range(self.ui.stat_table.rowCount()):
                    stat_num = self.ui.stat_table.item(row,1).data(QtCore.Qt.UserRole).toInt()[0]
                    item = [self.ui.stat_table.item(row,col).text().__str__() for col in range(col_count)] + [self._statistics[stat_num]['state'].to_string()]
                    f.write("\n" + ";".join(item))
            self.ui.statusbar.showMessage("Statistics data have been imported to file "+file_name, 1000*60)
    
    def build_chart(self):
        pass
    
    def update_timer(self):
        """Handles tick signal from running timer"""
        elapsed = self.elapsed_timer.elapsed() / 1000
        num_secs = elapsed % 60
        num_mins = elapsed / 60
        num_hrs = num_mins / 60
        if num_hrs>0:
            num_mins = num_mins % 60
        if num_hrs:
            self.timer_widget.setText('%02d:%02d:%02d'%(num_hrs,num_mins,num_secs))
        else:
            self.timer_widget.setText('%02d:%02d'%(num_mins,num_secs))
            
    def show_message(self, msg):
        """Show alert message box
        
        Args:
            msg:
        """
        msg_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Warning", msg, QtGui.QMessageBox.Ok, self)
        msg_box.exec_()
        
    def display_runtime_chart(self, value, best_value=float('inf')):
        """Display runtime chart
        
        Args:
            value: add new value point
            best_value: new best value point
        """
        if self.main_options['runtime_chart'] and not self._is_displaying_runtime:
            if self._chart_max_value<value:
                self._chart_max_value = value
            if self._chart_min_value>value:
                self._chart_min_value = value
            self._is_displaying_runtime = True
            self.ui.runtime_cost.setText("%.2f" % (value,))
            if best_value!=float('inf'):
                self.ui.best_cost.setText("%.2f" % (best_value,))
            
            scene = self.ui.runtime_chart.scene()
            if not scene:
                scene = QtGui.QGraphicsScene()
                width, height = 2, self._chart_max_value
            else:
                width, height = scene.sceneRect().width()+2, self._chart_max_value
            scene.setSceneRect(0,-height,width,height)
            sr = scene.sceneRect()
            h = value
            front_color, back_color = QtGui.QColor(0,127,0), QtGui.QColor(0,255,0)
            scene.addRect(sr.width()-2, -h, 2, h, QtGui.QPen(back_color), QtGui.QBrush(back_color))
            scene.addLine(sr.width()-1, -h, sr.width(), -h, QtGui.QPen(front_color))
            
#            if self._chart_prev_value!=None:
#                prev_h = int((sr.height()-self._chart_max_value*0.1)*self._chart_prev_value/self._chart_max_value)
#                scene.addLine(sr.width()-3, -prev_h, sr.width()-3, -h, QtGui.QPen(front_color))
                
            if best_value!=float('inf'):
                scene.addLine(sr.width()-2, -best_value, sr.width(), -best_value, QtGui.QPen(QtCore.Qt.red))
                if self._chart_prev_best_value!=float('inf'):
                    scene.addLine(sr.width()-3, -self._chart_prev_best_value, sr.width()-3, -best_value, QtGui.QPen(QtCore.Qt.red))
                
            self.ui.runtime_chart.setScene(scene)
            g = self.ui.runtime_chart_frame.geometry()
            if sr.width()>g.width():
                self.ui.runtime_chart.setGeometry(g.width()-sr.width(), 0, sr.width(), g.height())
            else:
                self.ui.runtime_chart.setGeometry(0, 0, sr.width(), g.height())
            self.ui.runtime_chart.fitInView(sr, QtCore.Qt.IgnoreAspectRatio)
            self._chart_prev_value = value
            self._chart_prev_best_value = best_value
            
            self._is_displaying_runtime = False
            
    def display_runtime_state(self, state, value):
        """Display actual runtime state as label
        
        Args:
            state: new state
            value: new state value
        """
        if not self._is_displaying_runtime_state:
            self._is_displaying_runtime_state = True
            self.display_board(state, has_solution=True)
            self._is_displaying_runtime_state = False
            
    def erase_runtime_chart(self):
        """Erase runtime chart"""
        self.ui.runtime_cost.setText("0.00")
        self.ui.best_cost.setText("0.00")
        scene = QtGui.QGraphicsScene()
        self.ui.runtime_chart.setScene(scene)
        self._chart_max_value = 0
        self._chart_min_value = float('inf')
        self._chart_prev_value = None
        self._chart_prev_best_value = float('inf')
                
if __name__ == "__main__":
    sys.path.append(join(sys.path[0], 'methods'))
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())
