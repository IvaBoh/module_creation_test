from odoo import models, fields


class HospitalPatientVisit(models.Model):
    _name = "hospital.visit"
    _description = "Patient visits to assigned physician"

    patient_id = fields.Many2one(comodel_name="patient", required=True)
    doctor_id = fields.Many2one(comodel_name="physician", required=True)
    diagnosis_id = fields.Many2many(
        comodel_name="disease", string="Detected diseases"
    )
    visit_date = fields.Date(required=True)
    case = fields.Text(required=False, string="Case notes")
