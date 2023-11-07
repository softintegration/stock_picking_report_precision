# -*- coding: utf-8 -*- 

import datetime

from odoo import models, fields, api, _
from odoo.addons.base.models.qweb import QWeb

CUSTOM_PRECISION_MODELS = ('stock.move','stock.move.line')
CUSTOM_PRECISION_REPORTS = ('stock.report_deliveryslip',)

class IrQWeb(models.AbstractModel, QWeb):
    _inherit = 'ir.qweb'

    def _get_field(self, record, field_name, expression, tagName, field_options, options, values):
        field = record._fields[field_name]

        # adds template compile options for rendering fields
        field_options['template_options'] = options

        # adds generic field options
        field_options['tagName'] = tagName
        field_options['expression'] = expression
        field_options['type'] = field_options.get('widget', field.type)
        inherit_branding = options.get('inherit_branding',
                                       options.get('inherit_branding_auto') and record.check_access_rights('write',
                                                                                                           False))
        field_options['inherit_branding'] = inherit_branding
        translate = options.get('edit_translations') and options.get('translatable') and field.translate
        field_options['translate'] = translate

        # field converter
        if values['xmlid'] not in CUSTOM_PRECISION_REPORTS:
            model = 'ir.qweb.field.' + field_options['type']
        elif record._name not in CUSTOM_PRECISION_MODELS:
            model = 'ir.qweb.field.' + field_options['type']
        elif field_options['type'] != 'float':
            model = 'ir.qweb.field.' + field_options['type']
        # FIXME:This elif case must be changed when we extend the scop of the module
        elif record.picking_type_id.digits < 0:
            model = 'ir.qweb.field.' + field_options['type']
        elif record.picking_type_id.digits > 0:
            field_options.update({'precision':record.picking_type_id.digits})
            model = 'ir.qweb.field.' + field_options['type']
        else:
            model = 'ir.qweb.field.integer'
        converter = self.env[model] if model in self.env else self.env['ir.qweb.field']

        # get content (the return values from fields are considered to be markup safe)
        content = converter.record_to_html(record, field_name, field_options)
        attributes = converter.attributes(record, field_name, field_options, values)

        return (attributes, content, inherit_branding or translate)



