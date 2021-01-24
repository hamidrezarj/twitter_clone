
console.log("Hello world.");


var likeBtns = document.getElementsByClassName("like_btn");

console.log(likeBtns);
for(let btn of likeBtns){

    btn.onclick = function (event) {
        let btn_state = btn.getAttribute("next-state");
        console.log("next-state: ", );
        if(btn_state === "Like"){
            // this.innerHTML = "Dislike";
            btn.setAttribute("next-state", "Dislike");
        }

        else {
            // this.innerHTML = "Like";
            btn.setAttribute("next-state", "Like");
        }

        // event.preventDefault();
        let form = $(this).closest("form");
        console.log('hey there');
        console.log("form", form);


        $.ajax({
            url: form.attr("change-data-url"),
            data: {
                'btn_value': $(this).val(),
                'btn_text': btn.getAttribute("next-state"),
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
