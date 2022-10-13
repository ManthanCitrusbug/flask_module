$(".delete-post").on("click", function(){
    var post_id = $(this).data("postid")
    if (confirm("Wanna delete this post?") === true){
        window.location.href = `/delete_post/${post_id}`
    }
})

$(".comment-button").on("click", function(){
    var post_id = $(this).data("postid")
    $(`.comment-form-${post_id}`).removeClass("d-none")
    $(this).hide()
    $(`#view-post-${post_id}`).hide()
})

$(".like-button").on("click", function(){
    var post_id = $(this).data("postid")
    window.location.href = `/like/${post_id}`
})

$(".dislike-button").on("click", function(){
    var likeid = $(this).data("likeid")
    window.location.href = `/dislike/${likeid}`
})