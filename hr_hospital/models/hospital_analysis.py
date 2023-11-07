from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalAnalysis(models.Model):
    _name = "hospital.analysis"
    _description = "Patient analysis card"

    sample = fields.Selection(
        selection=[
            ("blood", "Blood"),
            ("bone", "Bone"),
            ("CSF", "CSF"),
            ("soft_tissue", "Soft tissue"),
        ],
    )
    patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        required=False,
    )
