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
