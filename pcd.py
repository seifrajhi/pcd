#!/usr/bin/python
"""
    A simple application that shows how Bottle and jQuery get along.

    :copyright: (c) 2015 by Oz Nahum Tiram.
    :license: BSD, see LICENSE for more details.

    Inspired by the same example given in Flask
    :copyright: (c) 2015 by Armin Ronacher.
"""
app = None

import time
from bottle import route, run, debug, template, request
import json
from shinken.misc.sorter import hst_srv_sort
from shinken.util import safe_print
from shinken.misc.filter  import only_related_to
try:
    import json
except ImportError:
    # For old Python version, load
    # simple json (it can be hard json?! It's 2 functions guy!)
    try:
        import simplejson as json
    except ImportError:
        print "Error: you need the json or simplejson module"
        raise

# Our page
def get_page():
    # First we look for the user sid
    # so we bail out if it's a false one
    user = app.get_user_auth()

    if not user:
        app.bottle.redirect("/user/login")

    all_imp_impacts = only_related_to(app.datamgr.get_important_elements(), user)
    all_imp_impacts.sort(hst_srv_sort)
    #all_imp_impacts.sort(hst_srv_sort)

    #all_imp_impacts = app.datamgr.get_services() #important_elements()

    impacts = all_imp_impacts
    ## for imp in all_imp_impacts:
    ##     safe_print("FIND A BAD SERVICE IN IMPACTS", imp.get_dbg_name())
    ##     d = {'name': imp.get_full_name().encode('utf8', 'ignore'),
    ##          "title": "My Image 3", "thumb": "/static/images/state_flapping.png", "zoom": "/static/images/state_flapping.png",
    ##          "html": get_div(imp)}
    ##     impacts.append(d)

    # Got in json format
    #j_impacts = json.dumps(impacts)
    #print "Return impact in json", j_impacts
    all_pbs =  only_related_to(app.datamgr.get_all_problems(),user)
    now = time.time()
    # Get only the last 10min errors
    all_pbs = [pb for pb in all_pbs if pb.last_state_change > now - 600]
    # And sort it
    all_pbs.sort(hst_srv_sort)  # sort_by_last_state_change)

    return {'app': app, 'user': user, 'impacts': impacts, 'problems': all_pbs}

def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.params.get('a', 0, type=int)
    b = request.params.get('b', 0, type=int)
    return json.dumps({'result': a+b})



def bar(no):
    return template('pcd', request=request)



def index():
    return template('pcd', request=request)

pages = {get_page: {'routes': ['/pcd/', '/pcd'], 'view': 'pcd', 'static': True}}
debug(True)
run(port=8080)
