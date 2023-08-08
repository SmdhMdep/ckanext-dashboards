from ckan.plugins import toolkit

import ckanext.dashboards.db as db

def get_organisations():
    organization_list = toolkit.get_action('organization_list')({'ignore_auth': True}, {"limit": 1000 })

    print(organization_list)

    return organization_list

def get_datasets():
    package_list = toolkit.get_action('package_list')({'ignore_auth': True}, {"limit": 1000 })

    print(package_list)

    return package_list


def get_dashboards():

    pollCreationQueue = toolkit.get_action('pollCreationQueue')({'ignore_auth': True}, {})

    dashboardsInfo = db.dashboard.get_all()

    dashboardsList = []

    for dashboard in dashboardsInfo:
        #TODO: switch which adds colour to list
        dashboardsList.append(dashboard)

    print("Dashboard3 = ", dashboardsList)

    return dashboardsList