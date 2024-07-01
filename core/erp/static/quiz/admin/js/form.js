var fv;
var input_search_question;
var tblQuestions, tblSearchQuestions;
var quiz = {
    questions: [],
    getQuestionsIds: function () {
        return this.questions.map(value => value.id);
    },
    addQuestion: function (item) {
        this.questions.push(item);
        this.listQuestions();
    },
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
                {data: "id"},
                {data: "category.name"},
                {data: "description"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fas fa-times"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
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
                instructions: {
                    validators: {
                        notEmpty: {},
                    }
                },
                type: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un item'
                        },
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
            if (quiz.questions.length === 0) {
                message_error('Debe tener al menos 1 pregunta agregada en su banco de preguntas');
                return false;
            }
            parameters.append('questions', JSON.stringify(quiz.questions));
            submit_formdata_with_ajax('Alerta', '¿Estas seguro de guardar la siguiente encuesta?', pathname, parameters, function () {
                location.href = fv.form.getAttribute('data-url');
            });
        });
});

$(function () {
    input_search_question = $('input[name="input_search_question"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    $('select[name="type"]').on('change', function () {
        fv.revalidateField('type');
    });

    input_search_question.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_questions',
                    'term': request.term,
                    'ids': JSON.stringify(quiz.getQuestionsIds()),
                },
                dataType: "json",
                type: "POST",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            quiz.addQuestion(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearQuestions').on('click', function () {
        input_search_question.val('').focus();
    });

    $('#tblQuestions tbody')
        .off()
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblQuestions.cell($(this).closest('td, li')).index();
            quiz.questions.splice(tr.row, 1);
            tblQuestions.row(tr.row).remove().draw();
            $('.tooltip').remove();
        });

    $('.btnSearchQuestions').on('click', function () {
        tblSearchQuestions = $('#tblSearchQuestions').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_questions',
                    'term': input_search_question.val(),
                    'ids': JSON.stringify(quiz.getQuestionsIds()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "id"},
                {data: "category.name"},
                {data: "description"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="add" class="btn btn-success btn-flat btn-xs"><i class="fas fa-plus"></i></a>'
                    }
                }
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
        $('#myModalSearchQuestions').modal('show');
    });

    $('#myModalSearchQuestions').on('shown.bs.modal', function () {
        quiz.listQuestions();
    });

    $('#tblSearchQuestions tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var row = tblSearchQuestions.row($(this).parents('tr')).data();
            quiz.addQuestion(row);
            tblSearchQuestions.row($(this).parents('tr')).remove().draw();
        });

    $('.btnRemoveAllQuestions').on('click', function () {
        if (quiz.questions.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todo el banco de preguntas?', function () {
            quiz.questions = [];
            quiz.listQuestions();
        }, function () {

        });
    });
});