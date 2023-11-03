import calendar, datetime
from odoo import api, fields, models


class HospitalCreateSchedule(models.TransientModel):
    _name = "hospital.create.schedule"
    _description = "Create schedule"

    year = fields.Char(
        required=True,
        default="2023",
    )
    month = fields.Selection(
        selection=[
            (str(month), str(month_name[:3]))
            for month, month_name in enumerate(calendar.month_abbr)
            if month
        ],
        default="11",
        required=True,
    )
    week = fields.Selection(
        selection=[("even", "Even"), ("odd", "Odd")],
        required=True,
        default="even",
    )
    physician_id = fields.Many2one(
        comodel_name="hospital.physician",
        required=True,
    )
    monday = fields.Char(
        required=False, help="Input is the hours like '9,11,14,18'"
    )
    tuesday = fields.Char(
        required=False,
        help="Input is the hours like '9,11,14,18'",
        default="8",
    )
    wednesday = fields.Char(
        required=False, help="Input is the hours like '9,11,14,18'"
    )
    thursday = fields.Char(
        required=False, help="Input is the hours like '9,11,14,18'"
    )
    friday = fields.Char(
        required=False, help="Input is the hours like '9,11,14,18'"
    )

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
        self.ensure_one()

        days = {
            "monday": self.monday,
            "tuesday": self.tuesday,
            "wednesday": self.wednesday,
            "thursday": self.thursday,
            "friday": self.friday,
        }
        dates = self.get_dates(int(self.year), int(self.month), self.week)

        list_to_create = []
        for day, value in days.items():
            if value:
                hours = value.split(",")
                if hours:
                    for hour in hours:
                        for date in dates[day]:
                            list_to_create.append(
                                {
                                    "visit_date": date,
                                    "hour": hour,
                                    "physician_id": self.physician_id.id,
                                }
                            )

        for item in list_to_create:
            schedule_record = self.env["hospital.physician.schedule"].search(
                [
                    ("visit_date", "=", item["visit_date"]),
                    ("hour", "=", item["hour"]),
                    ("physician_id", "=", item["physician_id"]),
                ]
            )

            if not schedule_record:
                self.env["hospital.physician.schedule"].create(item)

    @staticmethod
    def get_dates(year, month, week):
        dates = {day.lower(): [] for day in calendar.day_name[:5]}

        first_day = datetime.date(year, month, 1)

        if week == "even":
            weeks = [
                i
                for i in range(
                    2, calendar.monthrange(year, month)[1] // 7 * 2 + 2, 2
                )
            ]
        else:
            weeks = [
                i
                for i in range(
                    1, calendar.monthrange(year, month)[1] // 7 * 2 + 1, 2
                )
            ]

        for week_num in weeks:
            week_start_date = first_day + datetime.timedelta(
                days=(week_num - 1) * 7 - first_day.weekday()
            )

            if week_start_date.month == month:
                for i in range(5):
                    date = week_start_date + datetime.timedelta(days=i)
                    dates[calendar.day_name[i].lower()].append(
                        date.strftime("%Y-%m-%d")
                    )

        return dates
