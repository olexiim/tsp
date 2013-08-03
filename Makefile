all: ui

ui: main_options.py main_window.py tsp_random_options.py

main_options.py: main_options.ui
	pyuic4 main_options.ui > main_options.py
main_window.py: main_window.ui
	pyuic4 main_window.ui > main_window.py
tsp_random_options.py: tsp_random_options.ui
	pyuic4 tsp_random_options.ui > tsp_random_options.py

