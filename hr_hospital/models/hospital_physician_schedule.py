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
        string="The physician who made a diagnosis",
        required=False,
    )

    @api.constrains("visit_date", "hour")
    def _check_visit_date(self):
        records = self.sudo().search_read(
            domain=[("id", "!=", self.id)], fields=["visit_date", "hour"]
        )

        for record in records:
            if fields.Date.to_date(self.visit_date) == record.get(
                "visit_date"
            ) and self.hour == record.get("hour"):
                raise ValidationError("Choose another date or time")

    def name_get(self):
        return [
            (tag.id, "%s: %s" % (tag.hour, tag.visit_date)) for tag in self
        ]
