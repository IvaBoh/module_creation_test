from odoo import models, fields


class HospitalAbstractPerson(models.AbstractModel):
    _name = "hospital.abstract.person"
    _description = "Abs model for related models"

    name = fields.Char()
    phone = fields.Char()
    email = fields.Char()
    photo = fields.Image(max_width=200, max_height=200)
    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
    )
