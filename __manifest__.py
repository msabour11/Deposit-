# -*- coding: utf-8 -*-
{
    'name': "Deposit Management System",

    'summary': "Deposit Management System",

    'description': """
       Deposit Management System to control transactions 
    """,

    'author': "Mohamed Abdelsabour",
    'website': "",

    'category': 'Productivity',
    'version': '0.1',

    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/bank_groups.xml',
        'security/transaction_record_rules.xml',
        'security/ir.model.access.csv',
        'data/bank_sequence.xml',
        'data/transaction_email_template.xml',
        'views/menus.xml',
        'views/bank_view.xml',
        'views/transaction_view.xml',
        'views/user_bank_view.xml',
    ],

}
