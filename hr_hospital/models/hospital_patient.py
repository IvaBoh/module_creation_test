from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Patient basic info"
    _inherit = "hospital.abstract.person"

    age = fields.Integer(
        required=True,
        compute="_compute_age_date",
        readonly=True,
        compute_sudo=True,
    )
    birthday_date = fields.Date(
        string="Date of Birth",
        required=True,
    )
    passport = fields.Char()
    physician_id = fields.Many2one(
        comodel_name="hospital.physician",
        string="Attending physician",
        required=False,
    )
    contact_person_ids = fields.One2many(
        comodel_name="hospital.contact.person",
        inverse_name="patient_id",
        required=False,
    )

    @api.depends("age", "birthday_date")
    def _compute_age_date(self):
        for record in self:
            if record.birthday_date:
                record.age = relativedelta(
                    datetime.now(), record.birthday_date
                ).years
            else:
                record.age = 0

    @api.model
    def create(self, vals):
        patient = super().create(vals)
        if vals.get("physician_id"):
            self.env["hospital.physician.assign.history"].create(
                {
                    "physician_id": vals.get("physician_id"),
                    "patient_id": patient.id,
                }
            )
        return patient

    def write(self, vals):
        for record in self:
            res = super().write(vals)
            if vals.get("physician_id"):
                record.env["hospital.physician.assign.history"].create(
                    {
                        "physician_id": record.physician_id.id,
                        "patient_id": record.id,
                    }
                )
            return res
