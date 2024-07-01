function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function message(text) {
    $.LoadingOverlay("show", {
        image: "",
        fontawesome: "fa fa-spinner fa-spin",
        custom: $("<div>", {
            css: {
                'font-family': "'Source Sans Pro', 'Helvetica Neue', Helvetica, Arial, sans-serif'",
                'font-size': '16px',
                'font-weight': 'normal',
                'text-align': 'center',
                'position': 'absolute',
                'top': '36%',
                'width': '100%',
            },
            text: text
        })
    });
    setTimeout(function () {
        $.LoadingOverlay("hide");
    }, 750);
}

function load_image(src) {
    Swal.fire({
        //title: 'Imagen',
        //text: src,
        imageUrl: src,
        imageWidth: '100%',
        imageHeight: 250,
        imageAlt: 'Custom image',
        animation: false,
    })
}

function loading_message(text) {
    $.LoadingOverlay("show", {
        image: "",
        fontawesome: "fas fa-circle-notch fa-spin",
        custom: $("<div>", {
            css: {
                'font-family': "'Source Sans Pro', 'Helvetica Neue', Helvetica, Arial, sans-serif'",
                'font-size': '16px',
                'font-weight': 'normal',
                'text-align': 'center',
                'position': 'absolute',
                'top': '36%',
                'width': '100%',
            },
            text: text
        })
    });
}

function alert_sweetalert(type, title, message, callback, timer, html) {
    Swal.fire({
        icon: type,
        title: title,
        text: message,
        html: html,
        grow: true,
        showCloseButton: true,
        allowOutsideClick: true,
        timer: timer
    }).then((result) => {
        callback();
    });
}

function message_error(message) {
    if (typeof (message) === "object") {
        var errors = '<ul style="list-style: square; text-align: left;">';
        $.each(message, function (index, item) {
            errors += '<li><b style="text-transform:capitalize;">' + index + "</b>.- " + item + '</li>';
        });
        errors += '</ul>';
        message = errors;
        alert_sweetalert('error', 'Error', "", function () {
        }, null, message);
        return false;
    }
    alert_sweetalert('error', 'Error', message, function () {
    }, null, "");
}

function submit_formdata_with_ajax_form(fv) {
    var submitButton = fv.form.querySelector('[type="submit"]');
    var parameters = new FormData(fv.form);
    $.confirm({
        // type: 'blue',
        theme: 'material',
        title: 'Confirmación',
        icon: 'fas fa-info-circle',
        content: '¿Esta seguro de realizar la siguiente acción?',
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: pathname,
                        data: parameters,
                        type: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                        success: function (request) {
                            console.log(request);
                            if (!request.hasOwnProperty('error')) {
                                location.href = fv.form.getAttribute('data-url');
                                return false;
                            }
                            message_error(request.error);
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                            message_error(errorThrown + ' ' + textStatus);
                        }
                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {
                    submitButton.removeAttribute('disabled');
                }
            },
        }
    });
}

function submit_formdata_with_ajax(title, content, url, parameters, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fas fa-info-circle',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url,
                        data: parameters,
                        type: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                        success: function (request) {
                            if (!request.hasOwnProperty('error')) {
                                callback(request);
                                return false;
                            }
                            message_error(request.error);
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                            message_error(errorThrown + ' ' + textStatus);
                        }
                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}

function submit_with_ajax(title, content, url, parameters, callback) {
    $.confirm({
        // type: 'blue',
        theme: 'material',
        title: title,
        icon: 'fas fa-info-circle',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: "btn-primary",
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url,
                        data: parameters,
                        type: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        dataType: 'json',
                        success: function (request) {
                            if (!request.hasOwnProperty('error')) {
                                callback();
                                return false;
                            }
                            message_error(request.error);
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                            message_error(errorThrown + ' ' + textStatus);
                        }
                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    });
}

function validate_form_text(type, event, regex) {

    var key = event.keyCode || event.which;
    var numbers = (key > 47 && key < 58) || key === 8;
    var numbers_spaceless = (key > 47 && key < 58);
    var letters = !((key !== 32) && (key < 65) || (key > 90) && (key < 97) || (key > 122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218)) || key === 8;
    var letters_spaceless = !((key < 65) || (key > 90) && (key < 97) || (key > 122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218)) || key === 8;
    var decimals = ((key > 47 && key < 58) || key === 8 || key === 46);

    if (type === 'numbers') {
        return numbers;
    } else if (type === 'letters') {
        return letters;
    } else if (type === 'numbers_letters') {
        return numbers || letters;
    } else if (type === 'letters_spaceless') {
        return letters_spaceless;
    } else if (type === 'letters_numbers_spaceless') {
        return letters_spaceless || numbers_spaceless;
    } else if (type === 'decimals') {
        return decimals;
    } else if (type === 'regex') {
        return regex;
    }
    return true;
}

function isNumber(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
}

function validate_decimals(el, evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode;
    var number = el.val().split('.');

    if (charCode !== 46 && charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    } else if (number.length > 1 && charCode === 46) {
        return false;
    } else if (el.val().length === 0 && charCode === 46) {
        return false;
    }

    return true;
}

function dialog_action(title, content, callback, cancel) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fas fa-info-circle',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: "btn-primary",
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    callback();
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {
                    cancel();
                }
            },
        }
    });
}