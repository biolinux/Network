/*
Description:
This JavaScript code enhances the functionality of a webpage by implementing dynamic post editing features. 
It relies on jQuery to facilitate DOM manipulation.

When a button with the class `edit-btn` is clicked, the code retrieves the ID of the corresponding post and its content.
It then hides elements with the class `view-mode` and `edit-mode`, and displays the `edit-mode` for the clicked post. 
Additionally, it hides the clicked `edit-btn` to prevent multiple simultaneous edits.

When a button with the class `save-btn` is clicked, the code retrieves the ID of the corresponding post and 
the new content entered by the user. It then sends an AJAX request to the server to update the post content. 
Upon successful response from the server, it updates the post content on the webpage, hides the `edit-mode`, 
shows the `view-mode`, and displays the `edit-btn` again for further edits.

This code allows users to edit posts inline without reloading the page, providing a seamless editing experience.
*/

$(document).ready(function() {
    $(".edit-btn").click(function() {
        // Retrieve post ID and content
        var postId = $(this).data("post-id");
        var postContent = $("#post-content-" + postId).text().trim();
        
        // Hide view mode and edit mode, show edit mode for the clicked post
        $(".view-mode").hide();
        $(".edit-mode").hide();
        $(this).siblings(".edit-mode").show();
        $(this).hide(); // Hide the edit button
    });

    $(".save-btn").click(function() {
        // Retrieve post ID and new content
        var postId = $(this).data("post-id");
        var newContent = $("#edit-content-" + postId).val().trim();

        // Retrieve CSRF token dynamically
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        
        // Send AJAX request to update post content
        $.ajax({
            url: `/edit-post/${postId}/`,
            type: "POST",
            data: {
                content: newContent,
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                // Update post content on the webpage
                $("#post-content-" + postId).text(newContent);
                $(".view-mode").show();
                $(".edit-mode").hide();
                $(`button[data-post-id="${postId}"].edit-btn`).show(); // Show the edit button again
            }
        });
    });
});


