function addProductToFavorites(productSlug) {
    $.ajax({
        url: '/user/add_to_favorites',
        type: 'GET',
        data: {
            'product_slug': productSlug
        },
        success: function(response) {
                alert("Действие выполнено!");
        },
        error: function() {

        }
    });
}


function switchPage(pageId, el) {
  var i, pages = document.getElementsByClassName("page");
  var buttons = document.getElementsByClassName("button");
  for (i = 0; i < pages.length; i++) {
    pages[i].style.display = "none";
    buttons[i].classList.remove("active");
  }
  document.getElementById(pageId).style.display = "block";
  el.classList.add("active");
}
