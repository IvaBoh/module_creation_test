from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalDisease(models.Model):
    _name = "hospital.disease"
    _description = "Disease general information"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"
    _order = "complete_name"

    name = fields.Char(index=True, required=True)
    complete_name = fields.Char(
        compute="_compute_complete_name",
        recursive=True,
        store=True,
    )
    parent_id = fields.Many2one(
        comodel_name="hospital.disease",
        string="Parent Category",
        index=True,
        required=False,
    )
    parent_path = fields.Char(index=True)
    child_id = fields.One2many(
        comodel_name="hospital.disease",
        inverse_name="parent_id",
        string="Child Categories",
    )
    description = fields.Char(required=False)
    symptoms = fields.Char(required=False)
    treatment = fields.Char(required=False)
    mortality = fields.Float(required=False)
    severity = fields.Selection(
        selection=[
            ("none", "None"),
            ("low", "Low"),
            ("moderate", "Moderate"),
            ("high", "High"),
        ],
        defult="none",
    )

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = "%s / %s" % (
                    category.parent_id.complete_name,
                    category.name,
                )
            else:
                category.complete_name = category.name

    @api.constrains("parent_id")
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create recursive categories."))

    @api.model
    def name_create(self, name):
        return self.create({"name": name}).name_get()[0]

    def name_get(self):
        if not self.env.context.get("hierarchical_naming", True):
            return [(record.id, record.name) for record in self]
        return super().name_get()
