from odoo import models, fields


class HospitalPhysician(models.Model):
    _name = "hospital.physician"
    _description = "Physician basic info"
    _inherit = "hospital.abstract.person"

    speciality = fields.Char()

    patient_ids = fields.One2many(
        comodel_name="hospital.patient",
        inverse_name="physician_id",
        string="Assigned patients",
    )
