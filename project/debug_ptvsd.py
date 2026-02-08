# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

import os
import ptvsd

# Only attach the debugger when we're the Django that deals with requests
try:
    ptvsd.enable_attach(address=('0.0.0.0', 3000), redirect_output=True)
except:
    pass
