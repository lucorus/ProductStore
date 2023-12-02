// Функции, работающие с корзиной в папке products


// добавляет продукт в корзину
function addProductToSession(productSlug) {
    $.ajax({
        url: '/user/add_basket',
        //url: '{% url "add_to_basket" %}',
        type: 'GET',
        data: {
            'product_slug': productSlug
        },
        success: function(response) {
            if (response.success) {
                // Обработка успешного добавления товара в сессию
            } else {
                // Обработка ошибки при добавлении товара в сессию
            }
        },
        error: function() {
            // Обработка ошибки AJAX запроса
        }
    });
}

// удаляет продукт с productSlug из корзины
function deleteProductFromBasket(productSlug) {
    $.ajax({
        //url: '{% url "delete_product_into_basket" %}',
        url: '/user/delete_product_into_basket',
        type: 'GET',
        data:
        {
            'product_slug': productSlug
        },
        success: function(response) {
            if (response.success) {
                // Обработка успешного удаления товара из сессии
            } else {
                // Обработка ошибки при удалении товара из сессии
            }
        },
        error: function() {
            // Обработка ошибки AJAX запроса
        }
    });
}
