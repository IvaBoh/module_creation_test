from datetime import timedelta

from odoo import models, fields, api, _
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
    start_date = fields.Datetime(
        compute="_compute_start_datetime", store=True, readonly=True
    )
    stop_date = fields.Datetime(
        compute="_compute_stop_datetime", store=True, readonly=True
    )

    @api.depends("visit_date", "hour")
    def _compute_start_datetime(self):
        for record in self:
            if record.visit_date and record.hour:
                combined_datetime_str = (
                    f"{record.visit_date} {int(record.hour):02d}:00:00"
                )
                record.start_date = fields.Datetime.from_string(
                    combined_datetime_str
                )
            else:
                record.start_date = False

    @api.depends("start_date")
    def _compute_stop_datetime(self):
        for record in self:
            if record.start_date:
                combined_datetime = fields.Datetime.from_string(
                    record.start_date
                )
                stop_datetime = combined_datetime + timedelta(minutes=50)
                record.stop_date = stop_datetime.strftime("%Y-%m-%d %H:%M:%S")
            else:
                record.stop_date = False

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
                    _(
                        "Selected physician appointment time "
                        "has already been occupied"
                    )
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
