# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields
from odoo.tools.float_utils import float_compare
from odoo.exceptions import ValidationError
from odoo.tools import profile

class Etudiant(models.Model):
    _name = "etudiant"

    partner_id = fields.Many2one('res.partner', auto_join=True)
    name = fields.Char(compute='_get_name', inverse='_set_name', search='_search_name')
    age = fields.Integer()
    majeur = fields.Boolean(compute="_get_majeur", search="_search_majeur")
    
    
    @api.depends('partner_id.name')
    def _get_name(self):
        for rec in self:
            rec.name = rec.partner_id.name
    @profile('profile.run')
    def _set_name(self):
        for rec in self:
            rec.partner_id.name = rec.name

    #@profile('profile.run')
    def _get_majeur_value(self):
        self.ensure_one()
        if self.age >= 18:
            return True
        else:
            return False

    @api.depends('age')
    def _get_majeur(self):
        for rec in self:
            rec.majeur = rec._get_majeur_value()
    
    def _search_name(self, operator, value):
        return [('partner_id.name', operator, value)]
    
    
    def _search_majeur(self, operator, value):
        if '!' in operator:
            value = not value
        if value:
            return [('age', '>=', 18)]
        else:
            return [('age', '<', 18)]

    @api.constrains('age')
    def _age_constraints(self):
        for rec in self:
            if rec.age < 16:
                raise ValidationError("Trop jeune")
        