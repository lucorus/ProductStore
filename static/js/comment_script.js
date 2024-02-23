function submitForm() {
        var form = document.getElementById('create-comment-form');
        var formData = new FormData(form);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/user/create_comment', true);
        xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                form.reset();
            }
        };
        xhr.send(formData);
        alert("Спасибо за ваш отзыв! \nВ скором времени он появится на сайте");
    }


function addProductToFavorites(productID) {
    $.ajax({
        url: '/user/add_to_favorites',
        type: 'GET',
        data: {
            'product_id': productID
        },
        success: function(response) {
                // Обработка успешного добавления товара в сессию
        },
        error: function() {
            // Обработка ошибки AJAX запроса
        }
    });
}