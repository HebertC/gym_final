
var ClientDashboard = (function () {

    var init;

    init = function () {
        $("#send-message").on('click', function () {

            var message = $("#message").val();
            $("#message-error").html('');
            if (!message) {
                $("#message-error").html('Error: message is empty!');
                return false;
            }
            var csrf = $("input[name='csrfmiddlewaretoken']").val();
            $("#send-message").text('SENDING...');
            $("#send-message").prop('disabled', 'disabled');
            $.ajax({
                url: $("#send-message-url").val(),
                data: {csrfmiddlewaretoken: csrf, message: message},
                method: 'POST',
                success: function (response) {
                    $("#total-messages").html(parseInt($("#total-messages").html()) + 1);
                    $("#message").val('');
                    $("#send-message").text('SEND MESSAGE');
                    $("#send-message").prop('disabled', null);
                    window.location.href = window.location.href;
                }
            });
            return false;
        });
        $(".chat-messages").animate({scrollTop: '500'}, 'slow');
    };

    return {
        init: init
    }
})();

$(document).ready(function () {
    if (window.location.pathname !== '/dashboard/') {
        return;
    }
    ClientDashboard.init();
});


$(document).ready(function () {
    if (window.location.pathname !== '/trainers/dashboard/') {
        return;
    }
    $("#clients-chat-list").find('a').on('click', function (e) {
        $("#active-chat-client-id").val($(e.target).data('user-id'));
        loadChatForSelectedClient();
    });

    if (!$("#active-chat-client-id").val()) {
        $("#active-chat-client-id").val($("#clients-chat-list").find('a:first').data('user-id'));
    }

    $("#send-message").on('click', function (e) {
        e.preventDefault();

$(document).ready(function () {

    function createAlertMessage() {
        return '<div class="row text-center"><div class="col-sm-offset-4 col-sm-4 disable-horizontal-padding"><div class="alert alert-success" role="alert">' +
            '<button type="button" class="close" data-dismiss="alert">×</button>' +
            '<strong>Well done!</strong> Message was sent. Thank you.' +
            '</div></div></div>';
    }

    $("#send-message").on('click', function () {


        var message = $("#message").val();
        $("#message-error").html('');
        if (!message) {
            $("#message-error").html('Error: message is empty!');
            return false;
        }

        var active_chat_user_id = $("#active-chat-client-id").val();
        var csrf = $("input[name='csrfmiddlewaretoken']").val();
        $("#send-message").text('SENDING...');
        $("#send-message").prop('disabled', 'disabled');
        $.ajax({
            url: '/trainers/send-client-message/',
            data: {csrfmiddlewaretoken: csrf, message: message, user_id: active_chat_user_id},
            method: 'POST',
            success: function (response) {
                $("#total-messages").html(parseInt($("#total-messages").html()) + 1);
                $("#message").val('');
                $("#send-message").text('SEND MESSAGE');
                $("#send-message").prop('disabled', null);
                window.location.href = "" + '?cu=' + active_chat_user_id;
            }
        });
        return false;
    });

    setTimeout(loadChatForSelectedClient, 300);
});

function loadChatForSelectedClient() {
    var active_chat_user_id = $("#active-chat-client-id").val();
    var csrf = $("input[name='csrfmiddlewaretoken']").val();
    $.ajax({
        url: '/trainers/get-user-chat/',
        data: {csrfmiddlewaretoken: csrf, user_id: active_chat_user_id},
        method: 'GET',
        success: function (response) {
            $("#chat").html(response);
            $(".chat-messages").animate({scrollTop: '500'}, 'slow');
        }
    });

}

        var csrf = $("input[name='csrfmiddlewaretoken']").val();

        $.ajax({
            url: $("#send-message-url").val(),
            data: {csrfmiddlewaretoken: csrf, message: message},
            method: 'POST',
            success: function (response) {
                $("#messages").html(createAlertMessage());
                $("#total-messages").html(parseInt($("#total-messages").html()) + 1);
                $("#message").val('');
            }
        });
        return false;
    })
});

