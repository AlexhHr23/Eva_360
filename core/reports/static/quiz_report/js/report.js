var select_quiz;
var tblUsers;
var report = {
    formatRow: function (items) {
        var content = '<table class="table"><thead class="thead-dark"><tr>';
        content += '<th scope="col">Categoría</th>';
        content += '<th scope="col">Pregunta</th>';
        content += '<th scope="col">Respuesta</th></tr></thead><tbody>';
        items.answers.forEach(function (value, index, array) {
            content += '<tr><td>' + value.quiz_detail.question.category.name + '</td>';
            content += '<td>' + value.quiz_detail.question.description + '</td>';
            content += '<td>' + (value.answer === -1 ? 'Sin responder': value.answer) + '</td></tr>';
        });
        content += '</tbody>';
        return content;
    },
    list: function () {
        $.ajax({
            url: pathname,
            data: {
                'action': 'search_report',
                'quiz': select_quiz.val(),
            },
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            success: function (request) {
                console.log(request);
                if (!request.hasOwnProperty('error')) {
                    tblUsers = $('#tblUsers').DataTable({
                        autoWidth: false,
                        destroy: true,
                        deferRender: true,
                        data: request.users,
                        columns: [
                            {"data": "user.names"},
                            {"data": "quiz.type.name"},
                            {"data": "user.dni"},
                            {"data": "status.name"},
                            {"data": "id"},
                        ],
                        columnDefs: [
                            {
                                targets: [-4],
                                class: 'text-center',
                                orderable: false,
                                render: function (data, type, row) {
                                    return data;
                                }
                            },
                            {
                                targets: [-1],
                                class: 'text-center',
                                orderable: false,
                                render: function (data, type, row) {
                                    return '<a rel="answers" class="btn btn-success btn-xs"><i class="fa-solid fa-clipboard-question"></i></a>';
                                }
                            },
                        ],
                        initComplete: function (settings, json) {
                            $(this).wrap('<div class="dataTables_scroll"><div/>');
                        }
                    });
                    Highcharts.chart('chart-answer', {
                        chart: {
                            plotBackgroundColor: null,
                            plotBorderWidth: null,
                            plotShadow: false,
                            type: 'pie'
                        },
                        title: {
                            text: 'Conteo total de respuestas por respuesta'
                        },
                        exporting: false,
                        tooltip: {
                            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                        },
                        accessibility: {
                            point: {
                                valueSuffix: '%'
                            }
                        },
                        plotOptions: {
                            pie: {
                                allowPointSelect: true,
                                cursor: 'pointer',
                                dataLabels: {
                                    enabled: true,
                                    format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                                }
                            }
                        },
                        series: [{
                            name: 'Porcentaje',
                            colorByPoint: true,
                            data: request.series
                        }]
                    });
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            }
        });
    }
};

$(function () {
    select_quiz = $('select[name="quiz"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_quiz.on('change', function () {
        report.list();
    });

    $('#tblUsers tbody')
        .off()
        .on('click', 'a[rel="answers"]', function () {
            var cell = tblUsers.cell($(this).closest('td, li')).index();
            var data = tblUsers.row(cell.row).data();
            var tr = $(this).closest('tr');
            var row = tblUsers.row(tr);
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                row.child(report.formatRow(data)).show();
                tr.addClass('shown');
            }
        });
});