var fv;
var tblQuestions;
var quiz = {
    questions: [],
    listQuestions: function () {
        tblQuestions = $('#tblQuestions').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.questions,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "quiz_detail.question.category.name"},
                {data: "quiz_detail.question.description"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var content = '';
                        [0, 1, 2, 3, 4].forEach(function (value, index, array) {
                            content += '<div class="form-check-inline"><label class="form-check-label">';
                            content += ' <input type="radio" class="form-check-input" value="' + value + '" name="question' + row.id + '">' + value;
                            content += '</label></div>';
                        });
                        return content;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    getAnswers: function () {
        return tblQuestions.rows().data().toArray();
    },
    validateAllAnswers: function () {
        var answers = tblQuestions.rows().data().toArray();
        console.log(answers);
        return $.isEmptyObject(answers.filter(value => value.answer === -1));
    }
};

document.addEventListener('DOMContentLoaded', function (e) {
    fv = FormValidation.formValidation(document.getElementById('frmForm'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                name: {
                    validators: {
                        notEmpty: {},
                    }
                },
                type: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tipo de encuesta'
                        },
                    }
                },
                instructions: {
                    validators: {
                        notEmpty: {},
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fv.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var parameters = new FormData(fv.form);
            if (!quiz.validateAllAnswers()) {
                message_error('Debe contestar todas las preguntas del cuestionario !!');
                return false;
            }
            parameters.append('answers', JSON.stringify(quiz.getAnswers()));
            submit_formdata_with_ajax('Alerta', '¿Estas seguro de terminar esta encuesta?', pathname, parameters, function () {
                location.href = fv.form.getAttribute('data-url');
            });
        });
});

$(function () {

    $('#tblQuestions tbody')
        .off()
        .on('change', 'input[type="radio"]', function () {
            var tr = tblQuestions.cell($(this).closest('td, li')).index();
            var data = tblQuestions.row(tr.row).data();
            data.answer = $(this).val();
        });
});
