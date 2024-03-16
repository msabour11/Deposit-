# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Bank(models.Model):
    _name = 'deposit.bank'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'Bank name already exists')]
    _description = 'deposit.system.Bank'

    name = fields.Char('Bank Name')
    code = fields.Char("Bank Code",readonly=True)
    description = fields.Text()
    address = fields.Many2one('res.partner', 'address')
    balance = fields.Float("Balance", compute="_compute_balance", store=True)
    transaction_ids = fields.One2many('deposit.transaction', 'bank_id', string="Transactions")
    customer_ids = fields.One2many('res.partner', 'bank_id', string="Customers")
    user_ids = fields.One2many('res.users', 'bank_id', string="Users")

    @api.model
    def create(self, vals):
        res = super(Bank, self).create(vals)
        res.code = self.env['ir.sequence'].sudo().next_by_code('bank_code')
        return res

    @api.depends('transaction_ids.amount', 'transaction_ids.transaction_type', 'transaction_ids.state')
    def _compute_balance(self):

        for bank in self:
            balance = 0.0
            for transaction in bank.transaction_ids:
                if transaction.state == 'confirm':
                    if transaction.transaction_type == 'deposit':
                        balance += transaction.amount
                    elif transaction.transaction_type == 'withdraw':
                        balance -= transaction.amount
            bank.balance = balance

