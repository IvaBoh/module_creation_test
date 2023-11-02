import calendar
from datetime import datetime, timedelta
from re import match

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDiseaseAnalyticReport(models.TransientModel):
    _name = "hospital.disease.analytic.report"
    _description = "Disease analytic report"

    year = fields.Char(
        required=True,
        default="2023",
    )
    month = fields.Selection(
        selection=[
            (str(month), str(month_name[:3]))
            for month, month_name in enumerate(calendar.month_abbr)
            if month
        ],
        default="11",
        required=True,
    )
    # record_ids = fields.Many2many(
    #     comodel_name="hospital.disease.data", string="Data records"
    # )

    @api.constrains("year")
    def _check_year_format(self):
        for record in self:
            if record.year and not match(r"^\d{4}$", record.year):
                raise ValidationError("Year format must be 4 digits.")

    def action_open_wizard(self):
        diagnoses = self.env["hospital.diagnosis"].search([])

        for record in diagnoses:
            self.env["hospital.disease.data"].create(
                {
                    "case_date": record.case_date,
                    "disease_id": record.disease_id.id,
                    "diagnose_id": record.id,
                }
            )

        # self.env["hospital.disease.data"].search([]).unlink()

        return {
            "name": "Create report for disease data",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "hospital.disease.analytic.report",
            "target": "new",
        }

    def action_create_report(self):
        self.ensure_one()

        first_day = datetime(int(self.year), int(self.month), 1).date()
        next_month = first_day.replace(month=first_day.month + 1, day=1)
        last_day = next_month - timedelta(days=1)

        records_by_date = self.env["hospital.disease.data"].search(
            [
                (
                    "case_date",
                    ">=",
                    first_day,
                ),
                (
                    "case_date",
                    "<=",
                    last_day,
                ),
            ]
        )

        result = {}
        for record in records_by_date:
            name = record.disease_id.name
            if name in result:
                result[name] += 1
            else:
                result[name] = 1
        return result
