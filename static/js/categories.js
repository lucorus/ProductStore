fetch('/get_categories')
            .then(response => response.json())
            .then(data => {
                const categories = data.results;
                const categoryContainer = document.getElementById('category-container');

                categories.forEach(category => {
                    const categoryElement = document.createElement('div');
                    categoryElement.classList.add('category');

                    const title = document.createElement('h3');
                    title.innerHTML = `<a href="${category.url}">${category.title}</a>`;
                    categoryElement.appendChild(title);

                    const image = document.createElement('img');
                    image.src = category.image;
                    categoryElement.appendChild(image);

                    const subcategories = document.createElement('ul');
                    category.subcategories.forEach(subcategory => {
                        const subcategoryItem = document.createElement('li');
                        const subcategoryLink = document.createElement('a');
                        subcategoryLink.href = subcategory.url;
                        subcategoryLink.textContent = subcategory.title;
                        subcategoryItem.appendChild(subcategoryLink);
                        subcategories.appendChild(subcategoryItem);
                    });

                    categoryElement.appendChild(subcategories);
                    categoryContainer.appendChild(categoryElement);
                });
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });