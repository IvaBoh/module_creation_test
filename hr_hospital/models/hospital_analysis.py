from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalAnalysis(models.Model):
    _name = "hospital.analysis"
    _description = "Patient analysis card"

    title = fields.Char()
    sample = fields.Selection(
        selection=[
            ("blood", "Blood"),
            ("bone", "Bone"),
            ("CSF", "CSF"),
            ("soft_tissue", "Soft tissue"),
        ],
    )
    analysis_date = fields.Date(
        required=False,
    )
    patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        required=False,
    )
    physician_id = fields.Many2one(
        comodel_name="hospital.physician",
        string="Computed Physician",
        compute="_compute_physician_id",
        store=True,
    )

    @api.depends("patient_id")
    def _compute_physician_id(self):
        for record in self:
            if record.patient_id:
                record.physician_id = record.patient_id.physician_id
            else:
                record.physician_id = False

    def name_get(self):
        return [
            (
                record.id,
                record.title,
            )
            for record in self
        ]
