from odoo import api, fields, models


class HospitalCreateSchedule(models.TransientModel):
    _name = "hospital.create.schedule"
    _description = "Create schedule"

    @api.model
    def action_open_wizard(self):
        return {
            "name": "Create schedule",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "hospital.create.schedule",
            "target": "new",
        }

    def action_create_schedule(self):
        pass
