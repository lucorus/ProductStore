fetch('/get_categories')
            .then(response => response.json())
            .then(data => {
                const categories = data.results;
                const categoryContainer = document.getElementById('category-container');

                categories.forEach(category => {
                    const categoryElement = document.createElement('div');
                    categoryElement.classList.add('category');

                    const title = document.createElement('h3');
                    title.innerHTML = `
                        <form action="/products" method="get">
                            <input type="hidden" name="category" value="${category.slug}">
                            <button class="btn btn-warning" type="submit">${category.title}</button>
                        </form>
                    `;
                    categoryElement.appendChild(title);

                    const image = document.createElement('img');
                    image.src = category.image;
                    categoryElement.appendChild(image);

                    const subcategories = document.createElement('ul');
                    category.subcategories.forEach(subcategory => {
                        subcategories.innerHTML += `
                            <li>
                                <form action="/products" method="get">
                                    <input type="hidden" name="subcategory" value="${ subcategory.slug }">
                                    <button class="btn btn-dark" type="submit">${ subcategory.title }</button>
                                </form>
                            </li>
                        `
                    });

                    categoryElement.appendChild(subcategories);
                    categoryContainer.appendChild(categoryElement);
                });
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });