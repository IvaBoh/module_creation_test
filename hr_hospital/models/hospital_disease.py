from odoo import models, fields


class HospitalDisease(models.Model):
    _name = "hospital.disease"
    _description = "Disease general information"

    title = fields.Char(required=True)
    description = fields.Char(required=True)
    symptoms = fields.Char(required=True)
    treatment = fields.Char(required=True)
    mortality = fields.Float(required=False)
