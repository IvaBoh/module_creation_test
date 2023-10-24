from odoo import models, fields


class HospitalPhysician(models.Model):
    _name = "hospital.physician"
    _description = "Physician basic info"

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    education = fields.Char(required=True)
    salary = fields.Float(required=True)
    experience = fields.Integer(required=True)
    address = fields.Char(required=True)
    patient_ids = fields.One2many(
        comodel_name="hospital.patient",
        inverse_name="physician_id",
        string="Assigned patients",
    )
