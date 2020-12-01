$(document).ready(function () {
    $("#user-avatar").on('change', function () {
        const file_name = $(this).val().replace(/^.*[\\\/]/, '')
        $(".custom-file-label").text(file_name);
    })
})
