from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class HospitalPatientVisitMulti(models.Model):
    _name = "hospital.patient.visit.multi"
    _description = "Patient visits to attending physician"

    visit_date = fields.Datetime(
        required=False,
        default=lambda self: fields.Datetime.now(),
    )
    treatment = fields.Char(required=True)
    patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        string="The patient who visits a physician",
        required=True,
    )
    physician_id = fields.Many2one(
        comodel_name="hospital.physician",
        string="The physician who examines a patient",
        required=True,
    )
    diagnosis_id = fields.Many2one(
        comodel_name="hospital.diagnosis",
        string="The diagnosed disease",
        required=False,
    )
    active = fields.Boolean(default=True)
    happened = fields.Boolean(default=False)
    visit_id = fields.Many2one(
        comodel_name="hospital.physician.schedule", string="Scheduled visit"
    )

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
    def _check_active(self):
        for record in self:
            if record.diagnosis_id and record.active is False:
                raise ValidationError(
                    "You can't archive record with diagnosis."
                )

    @api.constrains("visit_id")
    def _check_schedule_visit_date_availability(self):
        self.ensure_one()
        patient_visits = (
            self.env["hospital.patient.visit.multi"]
            .search([("id", "!=", self.id)])
            .mapped("visit_id")
        )

        if self.visit_id in patient_visits:
            raise ValidationError(
                "Selected physician appointment time "
                "has already been occupied"
            )

    def unlink(self):
        for visit in self:
            if visit.diagnosis_id:
                raise UserError(
                    "Deletion not allowed due to the existence of the "
                    "diagnosis."
                )
        return super(HospitalPatientVisitMulti, self).unlink()

    def name_get(self):
        return [
            (
                record.id,
                f"{record.patient_id.name} has a visit"
                f"on {record.visit_id.visit_date} at {record.visit_id.hour}:00 "
                f"to {record.physician_id.name}",
            )
            for record in self
        ]
