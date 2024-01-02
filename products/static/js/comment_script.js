function submitForm() {
        var form = document.getElementById('create-comment-form');
        var formData = new FormData(form);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '{% url "create_comment" %}', true);
        xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                console.log(response.comment_id);

                form.reset();
            }
        };
        xhr.send(formData);
        alert("Спасибо за ваш отзыв! \nВ скором времени он появится на сайте");
    }