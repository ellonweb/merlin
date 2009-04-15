import sys
import variables
import Core.modules
import Django.manage as D
if len(sys.argv) == 1:
    sys.argv.append("runserver")
D.execute_manager(D.settings)