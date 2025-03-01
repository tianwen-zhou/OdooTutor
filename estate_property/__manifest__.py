# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Estate Prperty Management',
    'version': '1.0',
    'category': 'Estate Prperty Management',  # Category for the App store
    'description': """
        Real Estate Management
    """,
    'depends': ['base'],
    # 'security': [
    #     'security/ir.model.access.csv',
    # ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_action.xml',
        'views/estate_property_view.xml',
        'views/estate_property_form.xml',
        'views/estate_property_search.xml',
        'views/estate_menus.xml',
        ],
    'application': True,
    'installable': True,
}