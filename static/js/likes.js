$(document).ready(function () {
    $(".like-dislike").each(function () {
        let upvote_pressed = false
        let downvote_pressed = false
        let post_rating = $(this).find(".post-rating")
        let upvote_button = $(this).find(".upvote-btn")
        let downvote_button = $(this).find(".downvote-btn")

        upvote_button.on('click', function () {
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
        })

        downvote_button.on('click', function () {
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
        })
    })
})