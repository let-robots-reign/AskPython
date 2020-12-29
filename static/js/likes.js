$(document).ready(function () {
    let cent = new Centrifuge('ws://127.0.0.1:8000/connection/websocket')
    cent.setToken($('#jwt_token').attr('data-token'))
    cent.subscribe('question_vote', function (msg) {
        addQuestionVote(msg)
    })
    cent.subscribe('answers_vote', function (msg) {
        addAnswerVote(msg)
    })

    cent.subscribe('new_answer', function(msg) {
        renderAlert(msg)
    })

    cent.connect()

    var vote_from_current_user = false

    $('.like-dislike').each(function () {
        let post_rating = $(this).find('.post-rating')
        let upvote_button = $(this).find('.upvote-btn')
        let downvote_button = $(this).find('.downvote-btn')

        let upvote_pressed = false
        let downvote_pressed = false
        if (upvote_button.hasClass('btn-success')) {
            upvote_pressed = true
        }
        if (downvote_button.hasClass('btn-danger')) {
            downvote_pressed = true
        }

        upvote_button.on('click', function () {
            vote_from_current_user = true
            const id = $(this).attr('data-id')
            const object_type = $(this).attr('data-type')

            $.post({
                url: '/vote/',
                data: {
                    id: id,
                    action: "upvote",
                    object_type: object_type
                }
            }).done(function (data) {
                if (data['redirect']) {
                    window.location = data['redirect'];
                } else {
                    if (!upvote_pressed) {
                        if (downvote_pressed) {
                            downvote_button.addClass('btn-secondary').removeClass('btn-danger')
                            post_rating.text(parseInt(post_rating.text()) + 1)
                            downvote_pressed = false
                        }
                        upvote_button.addClass('btn-success').removeClass('btn-secondary')
                        post_rating.text(parseInt(post_rating.text()) + 1)
                        upvote_pressed = true
                    } else {
                        // отменить голос
                        upvote_button.addClass('btn-secondary').removeClass('btn-success')
                        post_rating.text(parseInt(post_rating.text()) - 1)
                        upvote_pressed = false
                    }
                }
            })
        })

        downvote_button.on('click', function () {
            vote_from_current_user = true
            const id = $(this).attr('data-id')
            const object_type = $(this).attr('data-type')

            $.post({
                url: '/vote/',
                data: {
                    id: id,
                    action: "downvote",
                    object_type: object_type
                }
            }).done(function (data) {
                if (data['redirect']) {
                    window.location = data['redirect'];
                } else {
                    if (!downvote_pressed) {
                        if (upvote_pressed) {
                            upvote_button.addClass('btn-secondary').removeClass('btn-success')
                            post_rating.text(parseInt(post_rating.text()) - 1)
                            upvote_pressed = false
                        }
                        downvote_button.addClass('btn-danger').removeClass('btn-secondary')
                        post_rating.text(parseInt(post_rating.text()) - 1)
                        downvote_pressed = true
                    } else {
                        // отменить голос
                        downvote_button.addClass('btn-secondary').removeClass('btn-danger')
                        post_rating.text(parseInt(post_rating.text()) + 1)
                        downvote_pressed = false
                    }
                }
            })
        })
    })

    function addQuestionVote(msg) {
        if (!vote_from_current_user) {
            const data = msg['data']
            const currentRating = $(`#question-rating-${data['question_id']}`)
            if (data["mark"] === 1) {
                currentRating.text(parseInt(currentRating.text()) + 1)
            } else {
                currentRating.text(parseInt(currentRating.text()) - 1)
            }
        }
    }

    function addAnswerVote(msg) {
        if (!vote_from_current_user) {
            const data = msg['data']
            const currentRating = $(`#answer-rating-${data['answer_id']}`)
            if (data["mark"] === 1) {
                currentRating.text(parseInt(currentRating.text()) + 1)
            } else {
                currentRating.text(parseInt(currentRating.text()) - 1)
            }
        }
    }

    function renderAlert(msg) {
        $('#new-answers-alert').css('display', 'block')
    }
})