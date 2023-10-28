from odoo import models, fields


class HospitalPatientVisitMulti(models.Model):
    _name = "hospital.patient.visit.multi"
    _description = "Patient visits to attending physician"

    visit_date = fields.Datetime(
        required=True, default=lambda self: fields.Datetime.now()
    )
    treatment = fields.Char(required=True)
    patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        string="The patient who visits a physician",
    )
    physician_id = fields.Many2one(
        comodel_name="hospital.physician",
        string="The physician who examines a patient",
    )
    diagnosis_id = fields.Many2one(
        comodel_name="hospital.diagnosis",
        string="The diagnosed disease",
    )
