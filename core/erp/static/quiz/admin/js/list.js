var tblQuiz;
var quiz = {
    list: function () {
        var parameters = {
            'action': 'search',
        };
        tblQuiz = $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ""
            },
            order: [[0, 'asc']],
            columns: [
                {data: "number"},
                {data: "name"},
                {data: "type.name"},
                {data: "state"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data) {
                            return '<span class="badge badge-success badge-pill">Activo</span>';
                        }
                        return '<span class="badge badge-danger badge-pill">Inactivo</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '';
                        buttons += '<a rel="detail" class="btn btn-success btn-xs btn-flat" data-toggle="tooltip" title="Ver detalles"><i class="fa-solid fa-folder-open"></i></a> ';
                        if (!row.state) {
                            buttons += '<a rel="activate_quiz" class="btn btn-primary btn-xs btn-flat" data-toggle="tooltip" title="Activar encuesta"><i class="fa-solid fa-person-chalkboard"></i></a> ';
                            buttons += '<a href="' + pathname + 'update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        }
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                        return buttons;
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

$(function () {
    quiz.list();

    $('#data').addClass('table-sm');

    $('#data tbody')
        .off()
        .on('click', 'a[rel="activate_quiz"]', function () {
            var tr = tblQuiz.cell($(this).closest('td, li')).index();
            var row = tblQuiz.row(tr.row).data();
            submit_with_ajax('Alerta', '¿Estas seguro de aperturar la encuesta?', pathname, {
                'action': 'activate_quiz',
                'id': row.id,
            }, function () {
                alert_sweetalert('success', 'Alerta', 'La encuesta ya esta disponible para su resolución', function () {
                    tblQuiz.ajax.reload();
                }, 1500, null);

            })
        })
        .on('click', 'a[rel="detail"]', function () {
            $('.tooltip').remove();
            var tr = tblQuiz.cell($(this).closest('td, li')).index(),
                row = tblQuiz.row(tr.row).data();
            $('#tblQuestions').DataTable({
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
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "question.category.name"},
                    {data: "question.description"},
                ],
                columnDefs: [],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('.instructions').html(row.instructions);
            $('.nav-tabs a[href="#home"]').tab('show');
            $('#myModalQuestions').modal('show');
        });
})