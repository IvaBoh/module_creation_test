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

    def name_get(self):
        list_of_names = []
        for record in self:
            if record.patient_id and record.physician_id:
                list_of_names.append(
                    (
                        record.id,
                        f"{record.patient_id.name} assigned on "
                        f"{record.assignment_date} to "
                        f"{record.physician_id.name}",
                    )
                )
            else:
                list_of_names.append((record.id, record.assignment_date))
        return list_of_names
