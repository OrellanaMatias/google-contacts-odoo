# -*- coding: utf-8 -*-
{
    'name': "lpn_contact_module",

    'summary': """
        this is a http launcher possibility to push the odoo contact 
        list on an identified through oauth2 credentials gmail account """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Luc Pierson" ,
    'website': "http://bdm.lucpierson.com",
    "license": "AGPL-3",


    'category': 'Uncategorized',
    'version': '0.1',


    'depends': ['base'],


    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
