from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HospitalVisitReschedule(models.TransientModel):
    _name = "hospital.visit.reschedule"
    _description = "Reschedule a patient visit"

    visit_id = fields.Many2one(
        comodel_name="hospital.patient.visit.multi",
        domain=[
            ("happened", "=", False),
            ("visit_date", ">", fields.Datetime.now()),
        ],
        required=True,
        string="Your planed visit to change",
    )
    appointment_id = fields.Many2one(
        comodel_name="hospital.physician.schedule",
        domain=[("visit_date", ">", fields.Datetime.now())],
        required=True,
        string="New appointment to the same physician",
    )

    @api.constrains("visit_id", "appointment_id")
    def _check_physician(self):
        for record in self:
            if (
                record.visit_id.physician_id.id
                is not record.appointment_id.physician_id.id
            ):
                raise ValidationError("Select appointment with you physician.")

    @api.model
    def action_open_wizard(self):
        return {
            "name": "Visit Reschedule",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "hospital.visit.reschedule",
            "target": "new",
        }

    def action_reschedule(self):
        for record in self:
            record.visit_id.write({"visit_id": record.appointment_id.id})
            print(record.visit_id.visit_date)
            print(record.appointment_id.visit_date)
