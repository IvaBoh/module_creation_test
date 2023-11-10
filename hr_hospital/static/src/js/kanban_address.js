import field_registry from 'web.field_registry';
import AbstractField from 'web.AbstractField'
import  { qweb as QWeb, _t } from 'web.core';

var FieldKanbanAddress = AbstractField.extend({
    custom_template: "kanban_address",
    supportedFieldTypes: ['one2many', 'many2many'],
    fieldsToFetch: {
        name: {type: 'char'},
        district: {type: 'char'},
        display_name: {type: 'char'},
        eng_address: {type: 'char'},
    },

    _render: function () {
        var elements = this.value ? _.pluck(this.value.data, 'data') : [];
        this.$el.html(QWeb.render(this.custom_template, {elements: elements}));
    },
});

field_registry.add('kanban.kanban_address', FieldKanbanAddress);