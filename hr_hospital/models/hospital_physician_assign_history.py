from odoo import models, fields


class HospitalPhysicianAssignHistory(models.Model):
    _name = "hospital.physician.assign.history"
    _description = "Assignment change history of a physician"

    assignment_date = fields.Datetime(
        required=True,
        default=lambda self: fields.Datetime.now(),
    )
    patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        required=False,
    )
    physician_id = fields.Many2one(
        comodel_name="hospital.physician",
        required=False,
    )
