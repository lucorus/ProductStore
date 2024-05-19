document.addEventListener('DOMContentLoaded', function() {
    fetch('/products')
    .then(response => response.json())
    .then(data => {
        const nextPage = data.next;
        const previousPage = data.previous;
        const productList = document.getElementById('product-list');
        data.results.forEach(product => {
            const li = document.createElement('li');

            li.innerHTML =
            `
            <div class="product-details">
                <img src="${product.photo}" alt="фотка не загрузилась">
                <div>
                    <a style='margin-right: 1vh' href="${product.url}"><b>${product.title}</b></a>
                    <a style="margin-right: 1vh; color: green;" onclick="addProductInBasket('${product.slug}')" href="#">+</a>
                    <a onclick="deleteProductFromBasket('${product.slug}')" style="color: red" href="#">X</a>
                    <div class="product-price">${product.price - (product.price * (product.discount/100))}</div>
                    <div>Скидка на товар ${product.discount}%</div>
                    <div class="input-group mb-3">
                        <form action="/products" method="get">
                            <input type="hidden" name="category" value="${ product.subcategory.category.slug }">
                            <button class="btn btn-dark" type="submit">${ product.subcategory.category.title }</button>
                        </form>

                        <form style="margin-left: 2vh" action="/products" method="get">
                            <input type="hidden" name="subcategory" value="${ product.subcategory.slug }">
                            <button class="btn btn-dark" type="submit">${ product.subcategory.title }</button>
                        </form>
                    </div>
                </div>
            </div>
            `

            productList.appendChild(li);
        });
        if(previousPage)
        {
            const center = document.createElement('center');
            center.innerHTML = `<a href="${previousPage}">Предыдущая страница</a>`;
            productList.appendChild(center);
        }
        if(nextPage)
        {
            const center = document.createElement('center');
            center.innerHTML = `<a href="${nextPage}">Следующая страница</a>`;
            productList.appendChild(center);
        }
    })
    .catch(error => console.error('Error fetching data:', error));
});