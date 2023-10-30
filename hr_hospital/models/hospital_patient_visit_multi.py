from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class HospitalPatientVisitMulti(models.Model):
    _name = "hospital.patient.visit.multi"
    _description = "Patient visits to attending physician"

    visit_date = fields.Datetime(
        required=True,
        default=lambda self: fields.Datetime.now(),
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

    @api.onchange("visit_date", "physician_id")
    def _onchange_visit_date(self):
        old_visit_value = self._origin.visit_date
        date_old = fields.Datetime.to_datetime(old_visit_value)

        new_visit_value = self.visit_date
        date_new = fields.Datetime.to_datetime(new_visit_value)

        if not old_visit_value:
            if date_new < fields.Datetime.now():
                raise ValidationError(
                    "Select future visit date that is today or later"
                )

        if old_visit_value and date_old < fields.Datetime.now():
            raise ValidationError("You can't change expired visit.")

    @api.constrains("active")
    def check_active(self):
        if self.diagnosis_id and self.active is False:
            raise ValidationError("You can't archive record with diagnosis.")

    def unlink(self):
        for visit in self:
            if visit.diagnosis_id:
                raise UserError(
                    "Deletion not allowed due to the existence of the "
                    "diagnosis."
                )
        return super(HospitalPatientVisitMulti, self).unlink()
