function ShowProduct(productSlug)
{
     fetch('/product_api/' + productSlug)
    .then(response => response.json())
    .then(data => {
      document.getElementById('title').textContent += data.product.title;
      document.getElementById('price').textContent += data.product.price * ((100 - data.product.discount)/100) + ' руб.';
      document.getElementById('photo').src = data.product.photo;
      document.getElementById('category').textContent += data.product.subcategory.category.title;
      document.getElementById('subcategory').textContent += data.product.subcategory.title;
      document.getElementById('discount').textContent += data.product.discount + '%';
    })
    .catch(error => console.error('Ошибка:', error));
}
