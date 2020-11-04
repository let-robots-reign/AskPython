$(document).ready(function () {
    const form = $(".needs-validation")
    const validation = Array.prototype.filter.call(form, function (form) {
        form.addEventListener('submit', function (event) {
            if (form.checkValidity() === false) {
                event.preventDefault()
                event.stopPropagation()
            }
            form.classList.add("was-validated")
        }, false)
    })
})
