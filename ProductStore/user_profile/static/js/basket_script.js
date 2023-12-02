// изменяет кол-во продукта с productSlug +1 если oper = + и -1 иначе oper = -1
function ChangeCountFromBasket(productSlug, oper)
{
    $.ajax({
        //url: '{% url "change_count" %}',
        url: '/user/change_count',
        type: 'GET',
        data:
        {
            'product_slug': productSlug,
            'operation': oper
        },
        success: function(response)
        {
            if (response.success) {
                // Обработка успешного удаления товара из сессии
            }
            else {
                // Обработка ошибки при удалении товара из сессии
            }
        },
        error: function() {
            // Обработка ошибки AJAX запроса
        }
    });
}


// удаляет продукт с productSlug из корзины
function deleteProductFromBasket(productSlug)
{
    $.ajax({
        //url: '{% url "delete_product_into_basket" %}',
        url: '/user/delete_product_into_basket',
        type: 'GET',
        data:
        {
            'product_slug': productSlug
        },
        success: function(response)
        {
            if (response.success) {
                // Обработка успешного удаления товара из сессии
            }
            else {
                // Обработка ошибки при удалении товара из сессии
            }
        },
        error: function() {
            // Обработка ошибки AJAX запроса
        }
    });
}


// полностью очищает корзину
function ClearBasket()
{
    $.ajax({
        //url: '{% url "clear_basket" %}',
        url: '/user/clear_basket',
        type: 'GET',
        success: function(response)
        {
           if (response.success) {
            // Обработка успешного добавления товара в сессию
            }
            else {
              // Обработка ошибки при добавлении товара в сессию
            }
        },
        error: function() {
                // Обработка ошибки AJAX запроса
        }
    });
}
