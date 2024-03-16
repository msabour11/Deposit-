# -*- coding: utf-8 -*-
# from odoo import http


# class DepositSystem(http.Controller):
#     @http.route('/deposit_system/deposit_system', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/deposit_system/deposit_system/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('deposit_system.listing', {
#             'root': '/deposit_system/deposit_system',
#             'objects': http.request.env['deposit_system.deposit_system'].search([]),
#         })

#     @http.route('/deposit_system/deposit_system/objects/<model("deposit_system.deposit_system"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('deposit_system.object', {
#             'object': obj
#         })

