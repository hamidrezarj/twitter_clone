$(document).ready(function () {
    console.log("Ready");

    $("#follow").click(function (event) {
        event.preventDefault();

        let this_ = $(this);
        let url_ = this_.attr("change-data-url");
        $.ajax({
            url: url_,
            data: {},
            success: function (data) {
                if (data.followed) {
                    this_.text("Unfollow");
                    console.log(this_.text());
                } else {
                    this_.text("Follow");
                    console.log(this_.text());
                }

            }, error: function (error) {
                console.log("error: ", error);
            }
        })

    });


});