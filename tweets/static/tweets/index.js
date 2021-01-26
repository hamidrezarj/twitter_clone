console.log("Hello world.");

var myModal = document.getElementById('exampleModal');
var myInput = document.getElementById('exampleTrigger');
var mycloseBTN = document.getElementById('closeBTN');


// var editModal = document.getElementById('editModal');
var editModalTrigger = document.getElementById('editTrigger');
var editCloseBTN = document.getElementById('editCloseBTN');
window.addEventListener('load', (event) => {
    console.log("Listeners Added");
    // $(document).ready(function(){
    //     $('#editModal').modal("show");
    // });

    if (myInput) {
        myInput.onclick = ev => {
            $('#exampleModal').modal("show");
        }
    }
    if (mycloseBTN) {
        mycloseBTN.onclick = ev => {
            $('#exampleModal').modal("hide");
        }
    }

    if (editModalTrigger) {
        editModalTrigger.onclick = ev => {
            $('#editModal').modal("show");
        }
    }
    if (editCloseBTN) {
        editCloseBTN.onclick = ev => {
            $('#editModal').modal("hide");
        }
    }
    // $('#exampleModal').on('hidden.bs.modal', function (e) {
    //     console.log("hidden!")
    // })
});

// window.addEventListener('load', (event) => {
//     console.log("listener added")
//     myModal.addEventListener('shown.bs.modal', function () {
//       myInput.focus()
//     })
// });


$(document).ready(function () {
    $("#edit_form").submit(function (event) {
        console.log("clicked on submit");
        event.preventDefault();

        let editModal = $('#editModal');
        let fileChooser = $("#pfpFile");
        let fileChosen = false;
        // if (fileChooser.val() != "") {
        //     console.log("file chosen.");
        //     console.log("image selected: ", fileChooser.val());
        //     fileChosen = true;
        // } else {
        //     // raise error
        //     console.log("file not chosen.");
        //     editModal.modal("hide");
        // }

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        // if (fileChosen) {
        var formData = new FormData(this);
        let url_ = $(this).attr("change-profile-url");
        $.ajax({
            url: url_,
            type: "POST",
            data: formData,
            success: function (data) {
                console.log('data: ', data);
                // success
                if (data.updated) {
                    console.log("image saved successfully");
                    editModal.modal("hide");

                    let newUsername = $("#usernameChange").val();
                    //redirect to profile of updated user.
                    if (newUsername != "")
                        window.location.replace("/user/" + newUsername);
                    else
                        location.reload();
                } else {
                    //render error
                    console.log(data.form_error);
                    let errorContent = data.form_error.username[0];
                    let parent = document.getElementById("edit-username");
                    renderError(errorContent, parent)
                }
            },
            error: function (error) {
                console.log('error');
                console.log('error: ', error);
            },
            processData: false,
            contentType: false
        })
        // }

    });

});

function renderError(errorContent, parentElem) {
    console.log(errorContent);
    let errorElem = document.createElement('div');
    errorElem.classList.add("invalid-feedback");
    errorElem.classList.add("d-block");
    errorElem.innerHTML += errorContent;
    parentElem.appendChild(errorElem);
}


var likeBtns = document.getElementsByClassName("like_btn");

console.log(likeBtns);
for (let btn of likeBtns) {

    btn.onclick = function (event) {
        let btn_state = btn.getAttribute("next-state");
        console.log("next-state: ",);
        if (btn_state === "Like") {
            // this.innerHTML = "Dislike";
            btn.setAttribute("next-state", "Dislike");
        } else {
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
                if (data.has_changed) {
                    console.log("button value has been changed");
                }
                if (data.likes_count) {
                    //    change num of likes shown to user
                    form.next().children()[0].innerHTML = data.likes_count;
                }
            }
        });
    }
}
