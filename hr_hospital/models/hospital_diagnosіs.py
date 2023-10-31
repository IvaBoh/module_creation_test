from odoo import models, fields


class HospitalDiagnosis(models.Model):
    _name = "hospital.diagnosis"
    _description = "Diagnosis for specific patient by his physician"

    case_date = fields.Date(required=True)
    treatment = fields.Char(required=True)
    patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        string="The patient who was diagnosed",
        required=False,
    )
    physician_id = fields.Many2one(
        comodel_name="hospital.physician",
        string="The physician who made a diagnosis",
        required=False,
    )
    disease_id = fields.Many2one(
        comodel_name="hospital.disease",
        string="The diagnosed disease",
        required=False,
    )
    comment = fields.Text(required=False)
