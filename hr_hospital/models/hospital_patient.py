from odoo import models, fields


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Patient basic info"

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    address = fields.Char(required=True)
    physician_id = fields.Many2one(
        comodel_name="physician", string="Attending physician"
    )
    visit_ids = fields.One2many(comodel_name="visit", string="Visits")
    assurance = fields.Selection(
        selection=[
            ("basic", "Basic package"),
            ("standard", "Standard package"),
            ("silver", "Silver package"),
            ("golden", "Golden package"),
            ("platinum", "Platinum package"),
        ],
        default="Standard",
    )
