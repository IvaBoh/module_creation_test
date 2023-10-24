from odoo import models, fields


class HospitalVisit(models.Model):
    _name = "hospital.visit"
    _description = "Patient visits to assigned physician"

    patient_id = fields.Many2one(
        comodel_name="hospital.patient", required=True
    )
    physician_id = fields.Many2one(
        comodel_name="hospital.physician", required=True
    )
    diagnosis_id = fields.Many2many(
        comodel_name="hospital.disease", string="Detected diseases"
    )
    visit_date = fields.Date(required=True)
    case = fields.Text(required=False, string="Case notes")
