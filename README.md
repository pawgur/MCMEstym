# MCMEstym
# 09.10.2016 initial document created by pawelec

MCMpropagation.py this is the main component of the project. This is a Paython module which helps to evaluate uncertainty in measurement with the Monte Carlo method.

The rest of the objects are related to the simple GUI program Qt4 based, which is using the module mentioned. 
The GUI cntains following components:
- MCMmain.py this is the main GUI program,
- MCMWindow.py it describes the main GUI window class,
- MainDialog.py simple dialog window class,
- mplwidget.py this is the matplotlib widget for histogram drawing,
- multiCPU.py this the function used to determine number of cores for multiCPU processing,
- icons_rc.py source file for icons,
- help.html source file for help (not ready yet).
