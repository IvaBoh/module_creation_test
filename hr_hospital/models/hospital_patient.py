from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _


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
    physician_history_ids = fields.One2many(
        comodel_name="hospital.physician.assign.history",
        inverse_name="patient_id",
    )
    diagnosis_ids = fields.One2many(
        comodel_name="hospital.diagnosis",
        inverse_name="patient_id",
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

    def action_visit_history(self):
        self.ensure_one()
        return {
            "name": _("Patient visits"),
            "view_mode": "tree",
            "res_model": "hospital.patient.visit.multi",
            "type": "ir.actions.act_window",
            "target": "current",
        }

    def action_assignment_history(self):
        self.ensure_one()
        return {
            "name": _("Physician assignment history"),
            "view_mode": "tree,form",
            "res_model": "hospital.physician.assign.history",
            "type": "ir.actions.act_window",
            "target": "current",
        }

    def action_create_visit(self):
        self.ensure_one()
        return {
            "name": _("Create visit from patient form view"),
            "res_model": "hospital.patient.visit.multi",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_physician_id": self.physician_id.id,
                "default_patient_id": self.id,
            },
        }
