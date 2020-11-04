function validate_tags_string(tags) {
    const tags_number = tags.split(", ").length
    return tags_number > 0 && tags_number <= 3;
}

function validate_form(title, content, tags) {
    let is_correct = true;
    if (!title) {
        $("#invalid-title").css('visibility', 'visible');
        is_correct = false;
    }
    if (!content) {
        $("#invalid-content").css('visibility', 'visible');
        is_correct = false;
    }
    if (!tags) {
        $("#invalid-tags").css('visibility', 'visible');
        is_correct = false;
    } else if (!validate_tags_string(tags)) {
        $("#invalid-tags").text("Должно быть не более 3 тегов").css('visibility', 'visible');
        is_correct = false;
    }
    return is_correct;
}


$(document).ready(function() {
    $("#create-button").click(function() {
        const title = $("#input-title").val();
        const content = $("#input-content").val();
        const tags = $("#input-tags").val();

        const is_correct = validate_form(title, content, tags);
        if (is_correct) {
            document.location.href = "question.html"
        }
    })
})
