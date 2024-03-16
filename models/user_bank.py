# -*- coding: utf-8 -*-

from odoo import models, fields, api


class UserBank(models.Model):
    _inherit = 'res.users'

    bank_id = fields.Many2one('deposit.bank', string='Bank')
    transaction_ids = fields.One2many('deposit.transaction', 'user_id', string='Transactions')
    total_balance = fields.Float('Total Balance', compute='_compute_user_total_balance', store=True)
    bank_transactions = fields.One2many('deposit.transaction', compute='_compute_user_bank_transactions',
                                        string='Bank Transactions')

    @api.onchange('bank_id')
    def _compute_user_bank_transactions(self):
        for user in self:
            user.bank_transactions = user.bank_id.transaction_ids

    @api.depends('transaction_ids.amount', 'transaction_ids.transaction_type', 'transaction_ids.state', 'bank_id')
    def _compute_user_total_balance(self):

        for user in self:
            balance = 0.0
            for transaction in user.transaction_ids:
                if transaction.state == 'confirm':
                    if transaction.transaction_type == 'deposit' and transaction.bank_id == user.bank_id:
                        balance += transaction.amount
                    elif transaction.transaction_type == 'withdraw':
                        balance -= transaction.amount
            user.total_balance = balance


class PartnerBank(models.Model):
    _inherit = 'res.partner'
    bank_id = fields.Many2one('deposit.bank', string='Bank')
    # bank_transactions = fields.One2many('deposit.transaction', 'bank_id', string='Bank Transactions',
    #                                     related='bank_id.transaction_ids')
    transaction_ids = fields.One2many('deposit.transaction', 'customer', string='Transactions')
    total_balance = fields.Float('Total', compute='_compute_customer_total_balance', store=True)
    bank_transactions = fields.One2many('deposit.transaction', compute='_compute_bank_transactions',
                                        string='Bank Transactions')

    @api.onchange('bank_id')
    def _compute_bank_transactions(self):
        for partner in self:
            partner.bank_transactions = partner.bank_id.transaction_ids

    @api.depends('transaction_ids.amount', 'transaction_ids.transaction_type', 'transaction_ids.state', 'bank_id')
    def _compute_customer_total_balance(self):

        for partner in self:
            balance = 0.0
            for transaction in partner.transaction_ids:
                if transaction.state == 'confirm' and transaction.bank_id == partner.bank_id:
                    if transaction.transaction_type == 'deposit':
                        balance += transaction.amount
                    elif transaction.transaction_type == 'withdraw':
                        balance -= transaction.amount
            partner.total_balance = balance
