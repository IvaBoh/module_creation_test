from odoo import models, fields


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Patient"

    name = fields.Char(string="Name", required=True)
    attending_doctor_id = fields.Many2one(
        "hospital.doctor", string="Attending Doctor"
    )
    # Add other fields as needed
