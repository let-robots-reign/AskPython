$(document).ready(function () {
    $(".like-dislike").each(function() {
        const post_rating = $(this).find(".post-rating")
        $(this).find(".upvote-btn").on('click', function() {
            post_rating.text(parseInt(post_rating.text()) + 1)
        })
        $(this).find(".downvote-btn").on('click', function() {
            post_rating.text(parseInt(post_rating.text()) - 1)
        })
    })
})