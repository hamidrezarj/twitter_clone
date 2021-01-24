
console.log("Hello world.");

let likeBtns = $(".like_btn");
console.log(likeBtns);
for(let btn of likeBtns){

    btn.onclick = function (event) {
        if(this.innerHTML === "Like")
            this.innerHTML = "Dislike";
        else
            this.innerHTML = "Like";

        // event.preventDefault();
        let form = $(this).closest("form");
        console.log('hey there');
        console.log("form", form);


        $.ajax({
            url: form.attr("change-data-url"),
            data: {
                'btn_value': $(this).val(),
                'btn_text': btn.innerHTML,
            },
            dataType: 'json',
            success: function (data) {
                if(data.has_changed){
                    console.log("button value has been changed");
                }
                if(data.likes_count){
                //    change num of likes shown to user
                    form.next().children()[0].innerHTML = data.likes_count;
                }
            }
        });
    }
}

