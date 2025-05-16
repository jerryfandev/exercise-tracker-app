// Handle profile update form
$('#updateForm').on('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    $.ajax({
        url: '/main/profile',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            // Handle the success response
            alert('Profile updated successfully!');
            window.location.href = '/main/profile';
        },
        error: function(xhr) {
            // Handle the error response
            alert('Error updating profile: ' + xhr.responseText);
        }
    });
});
