/**
 * Document Title: Like Button Functionality
 * Author: Moise botsoe
 * Date: 22.04.2224
 * 
 * Description:
 * This JavaScript code provides functionality for a like button in a web application.
 * When a user clicks on a like button, an AJAX request is sent to the server to like/unlike a post.
 * The like count is updated accordingly, and the button text is toggled between "Like" and "Unlike".
 * 
 * Dependencies:
 * - jQuery library (Ensure jQuery is included in your HTML file before using this script)
 * 
 * Usage:
 * 1. Include jQuery library in your HTML file:
 *    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
 * 
 * 2. Add HTML markup for like buttons:
 *    <button class="like-btn" data-post-id="1">Like</button>
 *    <span id="like-count-1">10</span> Likes
 * 
 * 3. Include this JavaScript code in your HTML file or in a separate JS file:
 *    $(document).ready(function() {
 *        $(".like-btn").click(function() {
 *            // Code provided below
 *        });
 *    });
 * 
 * 4. Make sure your server-side code handles the AJAX request URL "/like-post/{postId}/" and responds with appropriate data.
 *    - The server should return JSON data with the updated like count and action ("like" or "unlike").
 */

$(document).ready(function() {
    $(".like-btn").click(function() {
        // Retrieve the post ID from the button's data attribute
        var postId = $(this).data("post-id");

        // Send an AJAX request to like/unlike the post
        $.ajax({
            url: `/like-post/${postId}/`, // Replace with your server's endpoint
            type: "POST",
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() // Include CSRF token for security
            },
            success: function(response) {
                // Update the like count on the page
                $("#like-count-" + postId).text(response.likes);

                // Toggle button text based on the action (like or unlike)
                if (response.action === 'like') {
                    $(this).text('Unlike');
                } else {
                    $(this).text('Like');
                }
            },
            error: function(xhr, status, error) {
                // Log any errors to the console
                console.error(xhr.responseText);
            }
        });
    });
});
