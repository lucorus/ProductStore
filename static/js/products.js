document.addEventListener('DOMContentLoaded', function() {
    fetch('/products')
    .then(response => response.json())
    .then(data => {
        const nextPage = data.next;
        const productList = document.getElementById('product-list');
        data.results.forEach(product => {
            const li = document.createElement('li');

            li.innerHTML =
            `
            <div class="product-details">
                <img src="${product.photo}" alt="фотка не загрузилась">
                <div>
                    <a href="${product.url}"><b>${product.title}</b></a><a style="color: green" onclick="addProductInBasket('${product.slug}')" href="#">+</a> <a onclick="deleteProductFromBasket('${product.slug}')" style="color: red" href="#">X</a>

                    <div class="product-price">${product.price - (product.price * (product.discount/100))}</div>
                    <div>Скидка на товар ${product.discount}%</div>
                    <a href="${product.subcategory.category.url}">${product.subcategory.category.title}</a>
                    <a href="${product.subcategory.url}">${product.subcategory.title}</a>
                </div>
            </div>
            `

            productList.appendChild(li);
        });
        if(nextPage)
        {
            const center = document.createElement('center');
            center.innerHTML = `<a href="${nextPage}">Следующая страница</a>`;
            productList.appendChild(center);
        }
    })
    .catch(error => console.error('Error fetching data:', error));
});