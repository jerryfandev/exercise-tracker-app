/*************************************************************
 * Handle login form                                         *
 *************************************************************/
$(function () {
    $('#login-form').on('submit', function (e) {
        e.preventDefault();

        const $username = $('#username');
        const $password = $('#password');
        const $failure = $('#unsuccessful-login');
        const $success = $('#successful-login');
        const $button = $('#login-button');
        const $spinner = $('#login-spinner');
        const $buttonText = $('#login-text');

        const formData = new FormData(this);

        $username.prop('disabled', true);
        $password.prop('disabled', true);
        $failure.addClass('d-none').text('');
        $success.addClass('d-none');
        $button.prop('disabled', true);
        $spinner.removeClass('d-none');
        $buttonText.addClass('d-none');

        fetch('/main/login', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': $('input[name="csrf_token"]').val()
            }
        })
            .then(response => response.json())
            .then(data => {
                // Simulate a delay for the spinner
                setTimeout(() => {
                    if (data.success) {
                        $success.removeClass('d-none');
                        window.location.href = '/main/dashboard';
                    } else {
                        $failure.removeClass('d-none')
                            .text(data.message || 'Invalid username or password!');
                    }

                    $username.prop('disabled', false);
                    $password.prop('disabled', false);
                    $button.prop('disabled', false);
                    $spinner.addClass('d-none');
                    $buttonText.removeClass('d-none');
                }, 2000);
            })
            .catch(error => {
                $failure.removeClass('d-none').text('Error occurred');
                $username.prop('disabled', false);
                $password.prop('disabled', false);
                $button.prop('disabled', false);
                $spinner.addClass('d-none');
                $buttonText.removeClass('d-none');
                console.error(error);
            });
    });
});
