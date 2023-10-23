from odoo import models, fields


class HospitalPatientVisit(models.Model):
    _name = "hospital.patient_visit"
    _description = "Patient Visits"

    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    diagnosed_disease_ids = fields.Many2many(
        "hospital.disease", string="Diagnosed Diseases"
    )
    visit_date = fields.Date(string="Visit Date", required=True)
    # Add other fields as needed
