/*************************************************************
 * This File is used to Handle register form                                      *
 *************************************************************/
$(function () {
    $('#register-form').on('submit', function (e) {
        e.preventDefault();
        const $error = $('#registration-error');
        const $success = $('#registration-success');
        const formData = new FormData(this);

        const $button = $('#register-button');
        const $spinner = $('#register-spinner');
        const $buttonText = $('#register-text');
        
        $error.addClass('d-none');
        $success.addClass('d-none');
        $button.prop('disabled', true);
        $spinner.removeClass('d-none');
        $buttonText.addClass('d-none');
        
        fetch('/main/register', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': $('input[name="csrf_token"]').val()
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // If registration is successful, show success message and redirect
                    $success.removeClass('d-none');
                    setTimeout(() => {
                        $button.prop('disabled', false);
                        $spinner.addClass('d-none');
                        $buttonText.removeClass('d-none');
                        window.location.href = '/main/login';
                    }, 2000);
                } else {
                    // If registration fails, show the error message
                    if (data.errors && data.errors.username && data.errors.username.includes('Username already exists')) {
                        $error.text('User has already existed, please choose another username.').removeClass('d-none');
                    } else if (data.errors && data.errors.email && data.errors.email.includes('Email already exists')) {
                        $error.text('Email has already been registered. Please use another email.').removeClass('d-none');
                    } else if (data.errors && data.errors.phone && data.errors.phone.includes('Phone number already exists')) {
                        $error.text('Phone number has already been registered. Please use another phone number.').removeClass('d-none');
                    } else {
                        $error.text(data.message || 'Registration failed!').removeClass('d-none');
                    }
                    $button.prop('disabled', false);
                    $spinner.addClass('d-none');
                    $buttonText.removeClass('d-none');
                }
            })
            .catch(error => {
                // Handle any errors that occur during the fetch
                $error.text('Error occurred during registration').removeClass('d-none');
                $button.prop('disabled', false);
                $spinner.addClass('d-none');
                $buttonText.removeClass('d-none');
                console.error(error);
            });
    });
});
