/*
Description:
This JavaScript code utilizes jQuery to enhance the functionality of a web form. The code is designed to handle the 
submission of a form with the ID `post-form`. When the user submits the form, instead of the default form submission 
behavior, the code intercepts the submission event and sends the form data asynchronously to a server-side endpoint 
(`/new_post/`) using AJAX (Asynchronous JavaScript and XML) technology.

The data sent to the server includes the content entered by the user into a textarea field with the ID `content`, 
as well as a CSRF (Cross-Site Request Forgery) token for security purposes. The expected response from the server 
is in JSON (JavaScript Object Notation) format.

Upon receiving a successful response from the server, the code dynamically generates HTML markup for a new post using 
the data returned by the server (such as author name, content, and timestamp), and prepends this new post 
to a designated area of the webpage. Additionally, it clears the content of the textarea field to allow the user 
to enter new content.

In case the server responds with an error, the code logs the error message to the browser console for debugging purposes.

This code enhances user experience by providing a seamless way to submit form data without refreshing the entire webpage, 
making the interaction smoother and more responsive.
*/

$(document).ready(function() {
    $('#post-form').submit(function(event) {
        event.preventDefault();  // Prevent the default form submission behavior
        
        var content = $('#content').val();  // Get the content from the textarea
        
        $.ajax({
            type: 'POST',
            url: '/new_post/',  // URL to the new_post view
            data: {
                'content': content,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()  // Include CSRF token
            },
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    // Prepend the newly created post to the top of the page
                    var postHtml = '<div class="post"><p><strong>' + response.post.author + '</strong></p><p>' + response.post.content + '</p><p>Posted on: ' + response.post.timestamp + '</p><p>Likes: 0</p></div><hr>';
                    $('.form-wrapper-1').prepend(postHtml);
                    // Clear the textarea
                    $('#content').val('');
                } else {
                    // Handle error response
                    console.error(response.error);
                }
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
});
