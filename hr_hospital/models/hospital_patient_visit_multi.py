from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class HospitalPatientVisitMulti(models.Model):
    _name = "hospital.patient.visit.multi"
    _description = "Patient visits to attending physician"

    visit_date = fields.Datetime(
        required=True,
        default=lambda self: fields.Datetime.now(),
        # compute="_compute_visit_date",
        # compute_sudo=True,
    )
    treatment = fields.Char(required=True)
    patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        string="The patient who visits a physician",
        required=False,
    )
    physician_id = fields.Many2one(
        comodel_name="hospital.physician",
        string="The physician who examines a patient",
        required=False,
    )
    diagnosis_id = fields.Many2one(
        comodel_name="hospital.diagnosis",
        string="The diagnosed disease",
        required=False,
    )
    active = fields.Boolean(default=True)

    # work
    # @api.constrains("visit_date")
    # def _check_visit_date(self):
    # today = fields.Datetime.today()
    # visit_value = fields.Datetime.to_datetime(self.visit_date)
    # if visit_value < today:
    #     raise ValidationError("Future visit date must be after today.")
    # self.check_expiration()

    # @api.constrains("visit_date")
    # def _check_visit_date(self):

    def check_expiration(self):
        today = fields.Datetime.today()
        visit_value = fields.Datetime.to_datetime(self.visit_date)
        if visit_value < today:
            raise ValidationError("Future visit date must be after today.")

    # def compare_dates(datetime_1, datetime_2):
    #     today = fields.Datetime.today()
    #     visit_value = fields.Datetime.to_datetime(self.visit_date)
    #     if visit_value < today:
    #         raise ValidationError("Future visit date must be after today.")

    @api.onchange("visit_date")
    def _onchange_visit_date(self):
        old_visit_value = self._origin.visit_date
        print(old_visit_value, "in change, old date")
        date_old = fields.Datetime.to_datetime(old_visit_value)

        new_visit_value = self.visit_date
        print(new_visit_value, "in change, new date")
        date_new = fields.Datetime.to_datetime(new_visit_value)

        # if date_old < date_new < fields.Datetime.today():
        #     raise ValidationError("You can't change expired visit date.")

    # def write(self, vals):
    #     print(self.visit_date, "In self")
    #     if "visit_date" in vals:
    #         value = fields.Datetime.to_datetime(vals["visit_date"])
    #         print(value, "In write")
    #         if value < datetime.now():
    #             print("old visit")
    #     #         raise ValidationError("Selected today's Date >>>>>>>>>>>>>>")
    #     return super(HospitalPatientVisitMulti, self).write(vals)

    # def update(self, vals):
    #     print(self.visit_date, "In self update")
    #     if "visit_date" in vals:
    #         print(vals["visit_date"], "In update")
    #     #     if fields.Date.to_date(vals["today_date"]) == fields.Date.today:
    #     #         raise ValidationError("Selected today's Date >>>>>>>>>>>>>>")
    #     return super(HospitalPatientVisitMulti, self).update(vals)

    # work
    # def unlink(self):
    #     for visit in self:
    #         if visit.diagnosis_id:
    #             raise UserError(
    #                 "Deletion not allowed due to the existence of the "
    #                 "diagnosis."
    #             )
    #     return super(HospitalPatientVisitMulti, self).unlink()
