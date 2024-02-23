$(document).ready(function() {
  $('#registrationForm').submit(function(event) {
    event.preventDefault(); // Отменить отправку формы

    var form = $(this);
    var url = form.attr('action');
    var formData = form.serialize();

    // Скрыть все сообщения об ошибках перед отправкой формы
    $('.error').text('');

    $.ajax({
      type: 'POST',
      url: url,
      data: formData,
      success: function(response) {
        // Обработка успешного ответа сервера
        console.log(response);
        if (response.status === 'success') {
          window.location.href = '{% url "main_page" %}'; // Редирект на страницу 'main_page'
        } else if (response.status === 'error') {
          // Вывести сообщения об ошибках рядом с соответствующими полями
          $.each(response.errors, function(field, error) {
            $('#' + field + 'Error').text(error);
          });
        } else {
          alert('Registration failed. Please try again.');
        }
      },
      error: function(xhr, errmsg, err) {
        // Обработка ошибки
        console.log(xhr.status + ': ' + xhr.responseText);
        alert('Registration failed. Please try again.');
      }
    });
  });
});


 var animateButton = function(e) {

  e.preventDefault;
  //reset animation
  e.target.classList.remove('animate');

  e.target.classList.add('animate');
  setTimeout(function(){
    e.target.classList.remove('animate');
  },700);
};

var bubblyButtons = document.getElementsByClassName("bubbly-button");

for (var i = 0; i < bubblyButtons.length; i++) {
  bubblyButtons[i].addEventListener('click', animateButton, false);
}
