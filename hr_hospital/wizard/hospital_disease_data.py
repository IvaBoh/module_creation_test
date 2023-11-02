from odoo import api, fields, models


class HospitalDiseaseData(models.TransientModel):
    _name = "hospital.disease.data"
    _description = "Disease analytic report"

    case_date = fields.Date()
    disease_id = fields.Many2one(
        comodel_name="hospital.disease",
        required=False,
    )
    diagnose_id = fields.Many2one(
        comodel_name="hospital.diagnosis",
        required=False,
    )

    @api.model
    def create(self, values):
        existing_record = self.env["hospital.disease.data"].search(
            [
                ("case_date", "=", values.get("case_date")),
                ("disease_id", "=", values.get("disease_id")),
                ("diagnose_id", "=", values.get("diagnose_id")),
            ]
        )

        if not existing_record:
            print("not exist")
            new_record = super().create(values)
            return new_record
        else:
            return existing_record
