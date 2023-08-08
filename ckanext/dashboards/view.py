from flask import Response
from flask.views import MethodView
from ckan.logic import NotFound, get_action
import ckan.lib.base as base
import ckan.logic as logic
import ckan.model as model
import ckan.lib.navl.dictization_functions as dict_fns

import ckan.plugins.toolkit as toolkit
from ckan.common import request,_
from flask import url_for

import ckan.lib.helpers as h
c = toolkit.c

#not all of these are required but these are the functions that you most likely will have to use to get the post working correctly
NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
check_access = logic.check_access
get_action = logic.get_action
tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
parse_params = logic.parse_params
flatten_to_string_key = logic.flatten_to_string_key

def add_dashboard():
    print("I AM IN THE VIEW!!!!")
    #Get the form data from the post request
    data_dict = clean_dict(
                dict_fns.unflatten(tuplize_dict(parse_params(request.form)))
            )

    #Create the required context
    context = {'model': model, 'session': model.Session, 'user_obj': c.user}

    print("Username = ", data_dict["Username"])
    print("organizationName = ", data_dict["organizationName"])
    print("datasetName = ", data_dict["datasetName"])
    print("URL = ", data_dict["Username"])

    #Send data to the action api
    dashboard = get_action(u'add_dashboard')(context, {
                u'Username': data_dict["Username"],
                u'organizationName': data_dict["organizationName"],
                u'datasetName': data_dict["datasetName"],
                u'URL': data_dict["URL"]
            })
    
    print("Dashboard2 = ", dashboard)

    #Give user some feedback that their comment has been added
    if (True):
        h.flash_notice(_(u'Added dashboard'))
    else:
        h.flash_notice(_(u'Invalid Comment. Ensure your comment is not empty and you are logged in.'))

    #redirect back to the correct page
    return h.redirect_to(url_for('dashboards.viewdashboards'))