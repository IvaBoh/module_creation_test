from odoo import models, fields, api
from odoo.exceptions import ValidationError


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

    @api.constrains("physician_id", "comment")
    def _check_comment(self):
        for record in self:
            print(record.comment)
            if not record.comment and record.physician_id.intern:
                raise ValidationError(
                    "Mentor must comment the intern diagnosis."
                )

    def name_get(self):
        return [
            (record.id, fields.Date.to_string(record.case_date))
            for record in self
        ]
