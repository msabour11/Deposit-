# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from odoo.tools.translate import _


class Transaction(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'deposit.transaction'
    _description = 'deposit.system.Transaction'

    name = fields.Char('Transaction Name')
    customer = fields.Many2one('res.partner', string='Customer')
    user_id = fields.Many2one('res.users', string='User')
    bank_id = fields.Many2one('deposit.bank', string='Bank')
    # bank_balance = fields.Float('Bank balance', related='bank_id.balance')
    amount = fields.Float("Amount")
    transaction_type = fields.Selection([('deposit', 'Deposit'), ('withdraw', 'Withdraw')])
    transaction_dates = fields.Datetime('Transaction Dates', default=fields.Datetime.now(), readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('pending', 'Pending'), ('confirm', 'Confirm')], string='Status',
                             default="draft")
    ref = fields.Char('Transaction Code')

    # related_bank_id = fields.Many2one('deposit.bank', related='customer.bank_id', string='Related Bank')

    def allowed_transaction_states(self, old_state, new_state):
        allowed = [('draft', 'confirm'), ('pending', 'confirm')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for record in self:
            if record.allowed_transaction_states(record.state, new_state):
                record.state = new_state
            else:
                msg = _(f'Moving from {record.state} to {new_state} is not allowed')
                raise UserError(msg)

    def make_confirm(self):
        for record in self:
            if record.transaction_type == 'withdraw' and record.bank_id.balance < record.amount:
                raise UserError('Not enough balance to withdraw')
            record.change_state('confirm')
            template = self.env.ref('deposit_system.email_template_transaction_done')
            print(template)
            template.send_mail(record.id)
            print(template.send_mail(record.id))

    # total_amount = fields.Float("Total Amount")
    @api.constrains('amount', 'state')
    def check_bank_balance(self):
        for record in self:
            if record.state == 'confirm' and record.transaction_type == 'withdraw':
                if record.bank_id.balance < record.amount:
                    raise ValidationError('Not enough balance to withdraw')

    def unlink(self):

        for record in self:
            if record.state == 'confirm':
                raise ValidationError("Cannot delete transaction in 'confirm' state.")

        return super(Transaction, self).unlink()

    def write(self, vals):
        for record in self:
            if record.state == 'confirm':
                raise UserError('Cannot update a confirmed transaction')
        return super(Transaction, self).write(vals)

    @api.model
    def create(self, vals):
        res = super(Transaction, self).create(vals)
        res.ref = self.env['ir.sequence'].sudo().next_by_code('transaction_code')
        res['state'] = 'pending'
        print(res.ref)
        print(res.state)
        return res
