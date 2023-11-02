from odoo import api, fields, models


class HospitalDiseaseCount(models.TransientModel):
    _name = "hospital.disease.count"
    _description = "Disease count for certain month and date"

    case_date = fields.Date()
    disease_id = fields.Many2one(
        comodel_name="hospital.disease",
        required=False,
    )
    diagnose_id = fields.Many2one(
        comodel_name="hospital.diagnosis",
        required=False,
    )
