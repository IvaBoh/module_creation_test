from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HospitalPhysicianSchedule(models.Model):
    _name = "hospital.physician.schedule"
    _description = "Schedule of a physician"

    visit_date = fields.Date(required=False, default=fields.Date.context_today)
    hour = fields.Selection(
        [(str(hour), f"{hour:02d}.00") for hour in range(8, 19)],
        required=False,
    )
    physician_id = fields.Many2one(
        comodel_name="hospital.physician",
        required=False,
    )

    @api.constrains("visit_date", "hour", "physician_id")
    def _check_visit_date(self):
        self.ensure_one()
        records = self.sudo().search_read(
            domain=[("id", "!=", self.id)],
            fields=["visit_date", "hour", "physician_id"],
        )

        for record in records:
            if (
                fields.Date.to_date(self.visit_date)
                == record.get("visit_date")
                and self.hour == record.get("hour")
                and self.physician_id.id == record.get("physician_id")[0]
            ):
                raise ValidationError(
                    "Selected physician appointment time "
                    "has already been occupied"
                )

    def name_get(self):
        return [
            (
                record.id,
                "%s:00 %s %s "
                % (record.hour, record.visit_date, record.physician_id.name),
            )
            for record in self
        ]
