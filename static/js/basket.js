// Функции, работающие с корзиной


function addProductInBasket(productSlug) {
    $.ajax({
        url: '/basket/basket_add/' + productSlug,
        type: 'GET'
    });
}


function deleteProductFromBasket(productSlug) {
    $.ajax({
        url: '/basket/delete/' + productSlug,
        type: 'GET'
    });
}


// изменяет кол-во продукта с productSlug +-1 если oper = '-' иначе +1
function ChangeCountFromBasket(productSlug, oper)
{
    $.ajax({
        url: '/basket/change_count/' + productSlug + '/' + oper,
        type: 'GET',
    });
}
