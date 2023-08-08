import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from flask import Blueprint

import ckan.model as model

import ckanext.dashboards.db as db
import ckanext.dashboards.helpers as helpers
import ckanext.dashboards.view as view
import ckanext.dashboards.actionapi as actionapi


c = toolkit.c

def dataset_dashboard(package_type,id):
    data_dict = {"id": id}
    context = {'model': model, 'user': c.user, 'auth_user_obj': c.userobj}
    pkg_dict = toolkit.get_action("package_show")(context, data_dict)

    return toolkit.render(
        "package/dashboard.html",
        {
            "pkg_dict": pkg_dict,
            "id": id  # i.e. package's current name
        },
    )

def dashboard_form():
    return toolkit.render(
        "dashboard/dashboard-form.html"
    )

def dashboard_view():
    return toolkit.render(
        "dashboard/dashboard-view.html"
    )


    #TODO: add exception
    #except toolkit.NotAuthorized:
    #    return toolkit.abort(403, 'Need to be system administrator to administer')


class DashboardsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPluginObserver, inherit=True)

    # IConfigurable
    def configure(self, config):
        #db.dashboards_table.drop()
        #db.dashboard_template_table.drop()
        # if not db.dashboards_table.exists():
        #     db.dashboards_table.create()
        if not db.dashboards_table.exists():
            db.dashboards_table.create()


    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets', 'dashboards')
        
    # IBlueprint
    def get_blueprint(self):
        u'''Return a Flask Blueprint object to be registered by the app.'''
        # Create Blueprint for plugin
        blueprint = Blueprint(self.name, self.__module__)
        blueprint
        blueprint.template_folder = 'templates'

        rules = [
            ('/dashboard/form', 'formdashboards', dashboard_form),
            ('/dashboard/view', 'viewdashboards', dashboard_view)
        ]
        for rule in rules:
            blueprint.add_url_rule(*rule)

        blueprint.add_url_rule('/dashboard/add', 'adddashboards', methods=[u'POST'], view_func=view.add_dashboard)

        return blueprint
    
    # IActions
    def get_actions(self):
        actions_dict = {
            'add_dashboard': actionapi.add_dashboard,
            "pollCreationQueue": actionapi.pollCreationQueue
        }   
        return actions_dict
    
    # ITemplateHelpers
    def get_helpers(self):
        return {
            'get_organisations': helpers.get_organisations,
            'get_datasets': helpers.get_datasets,
            "get_dashboards": helpers.get_dashboards
            }