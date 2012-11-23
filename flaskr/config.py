DATABASE = '/tmp/flaskr.db'
SECRET_KEY = "6(!<HIbsAo>e{#@>`WRW3OC21svML`_-t0/"
USERNAME = 'admin'
PASSWORD = 'default'

try:
    from flaskr.config_local import *
except ImportError:
    pass
