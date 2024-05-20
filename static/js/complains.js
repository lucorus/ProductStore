function CreateComplain(commentId) {
    $.ajax({
        url: '/user/create_complaint',
        type: 'GET',
        data: {
            "comment_id": commentId
        },
        success: function(response) {
            alert("Действие выполнено!");
        },
        error: function() {
            alert("Произошла неизвестная ошибка")
        }
    });
}