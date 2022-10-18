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

$(".delete-user").on("click", function(){
    var user_id = $(this).data("userid")
    if (confirm("Wanna delete this user?") === true){
        window.location.href = `/customadmin/${user_id}/delete_user`
    }
})

$(".delete-post-customadmin").on("click", function(){
    var post_id = $(this).data("postid")
    if (confirm("Wanna delete this post?") === true){
        window.location.href = `/customadmin/${post_id}/delete_post`
    }
})

$(".delete-like-customadmin").on("click", function(){
    var like_id = $(this).data("likeid")
    if (confirm("Wanna delete this post?") === true){
        window.location.href = `/customadmin/${like_id}/delete_like`
    }
})