# MCMEstym
//09.10.2016 initial document created by pawelec
//06.11.2016 the project is under private redevelopment, not all components are available for the time being. 

MCMpropagation.py this is the main component of the project. This is a Paython module which helps to evaluate uncertainty in measurement with the Monte Carlo method.

The rest of the objects are related to the simple GUI program Qt4 based, which is using the module mentioned. 
The GUI contains the following components:
- MCMmain.py this is the main GUI program,
- MCMWindow.py it describes the main GUI window class,
- MainDialog.py simple dialog window class,
- mplwidget.py this is the matplotlib widget for histogram drawing,
- multiCPU.py this the function used to determine number of cores for multiCPU processing,
- icons_rc.py source file for icons,
- help.html source file for help (not ready yet).

iPython_script.txt - this is very basic script which you can run with iPython, it showing how to use the main module in order to calculate all necessary values to evaluate an uncertainty in measurement.
