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
                {data: "quiz.number"},
                {data: "date_joined"},
                {data: "quiz.name"},
                {data: "status"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        switch (row.status.id) {
                            case "to_resolve":
                                return '<span class="badge badge-info badge-pill">' + row.status.name + '</span>';
                            case "resolved":
                                return '<span class="badge badge-success badge-pill">' + row.status.name + '</span>';
                        }
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '';
                        buttons += '<a rel="detail" class="btn btn-success btn-xs btn-flat"><i class="fa-solid fa-folder-open"></i></a> ';
                        if (row.status.id === 'to_resolve') {
                            buttons += '<a href="' + pathname + 'answers/' + row.quiz.access_key + '/" class="btn btn-primary btn-xs btn-flat"><i class="fa-solid fa-marker"></i></a> ';
                        }
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
                    {data: "quiz_detail.question.category.name"},
                    {data: "quiz_detail.question.description"},
                    {data: "answer"},
                ],
                columnDefs: [
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            if (data === -1) {
                                return 'Sin resolver';
                            }
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('.instructions').html(row.quiz.instructions);
            $('.nav-tabs a[href="#home"]').tab('show');
            $('#myModalQuestions').modal('show');
        });
})