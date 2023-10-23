from odoo import models, fields


class HospitalDisease(models.Model):
    _name = 'hospital.disease'
    _description = 'Disease Types'

    name = fields.Char(string='Name', required=True)
    # Add other fields as needed
