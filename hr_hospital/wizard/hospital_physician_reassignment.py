from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HospitalPhysicianReassignment(models.TransientModel):
    _name = "hospital.physician.reassignment"
    _description = "Physician reassignment"

    physician_id = fields.Many2one(
        comodel_name="hospital.physician", required=True
    )
    patient_ids = fields.Many2many(
        comodel_name="hospital.patient", string="Patients"
    )

    @api.model
    def action_open_wizard(self):
        return {
            "name": _("Physician reassignment"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "hospital.physician.reassignment",
            "target": "new",
        }

    def action_reassignment(self):
        self.ensure_one()
        for record in self.env["hospital.patient"].browse(
            self.env.context["active_ids"]
        ):
            record.write({"physician_id": self.physician_id.id})
