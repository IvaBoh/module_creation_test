from odoo import models, fields


class HospitalContactPerson(models.Model):
    _name = "hospital.contact.person"
    _description = "A person who may act on behalf of a patient."
    _inherit = "hospital.abstract.person"

    patient_id = fields.Many2one(
        comodel_name="hospital.patient",
    )
