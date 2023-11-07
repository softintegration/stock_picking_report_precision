# -*- coding: utf-8 -*- 

import datetime

from odoo import models, fields, api, _


class PickingType(models.Model):
    _inherit = 'stock.picking.type'

    digits = fields.Integer('Digits',default=-1,help="This is the number of digits for all the float fields in delivery of this operation type,-1 mean that we ignore this setting")




