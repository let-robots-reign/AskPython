$(document).ready(function () {
    $('.correct-checkbox').each(function () {
        $(this).on('click', function () {
            let checkbox = $(this)
            let answer_id = checkbox.attr('data-answer-id')
            let related_question_id = checkbox.attr('data-question-id')
            $(`#mark-error-${answer_id}`).empty()
            $.post({
                url: '/mark_correct/',
                data: {
                    qid: related_question_id,
                    ansid: answer_id
                }
            }).done(function (data) {
                if (data['error']) {
                    $(`#mark-error-${answer_id}`).text(data['error'])
                    checkbox.prop('checked', false)
                } else if (checkbox.is(':checked')) {
                    $(`#label-${answer_id}`).text('Вы отметили этот ответ как правильный').css('color', 'green')
                } else {
                    $(`#label-${answer_id}`).text('Отметить как решение').css('color', 'black')
                }
            })
        })
    })
})