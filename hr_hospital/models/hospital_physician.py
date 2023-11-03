from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalPhysician(models.Model):
    _name = "hospital.physician"
    _description = "Physician basic info"
    _inherit = "hospital.abstract.person"

    speciality = fields.Char()

    patient_ids = fields.One2many(
        comodel_name="hospital.patient",
        inverse_name="physician_id",
        string="Assigned patients",
        required=False,
    )
    intern = fields.Boolean(default=False, required=False)
    mentor_id = fields.Many2one(
        comodel_name="hospital.physician",
        string="Mentor physician",
        required=False,
    )

    @api.constrains("mentor_id")
    def _check_mentor_id(self):
        if self.mentor_id and self.mentor_id.intern:
            raise ValidationError(_("You can't choose an intern as a mentor."))

    def name_get(self):
        list_of_names = []
        for record in self:
            if record.intern:
                list_of_names.append((record.id, f"{record.name} | Intern "))
            else:
                list_of_names.append((record.id, record.name))
        return list_of_names
