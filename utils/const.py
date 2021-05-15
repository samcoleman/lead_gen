#import os

#__CUR_DIR__ = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

import os, sys
# determine if the application is a frozen `.exe` (e.g. pyinstaller --onefile)
if getattr(sys, 'frozen', False):
    __CUR_DIR__ = os.path.dirname(sys.executable)
# or a script file (e.g. `.py` / `.pyw`)
elif __file__:
    __CUR_DIR__ = os.path.dirname(os.path.dirname(__file__))
