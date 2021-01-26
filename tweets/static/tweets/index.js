console.log("Hello world.");

function OnInput() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
}

function validateTweetBox() {
    var len = tweetBox.value.length;
    return (tweetBox.minLength < len && tweetBox.maxLength > len);
}

function changeSubmit() {
    if (!validateTweetBox()) {
        tweetBoxSubmit.disabled = true;
    } else {
        tweetBoxSubmit.disabled = false;
    }
}

var tweetBox = document.getElementById('postBox');
var tweetBoxSubmit = document.getElementById('postTweetBtn');
if (tweetBox) {
    tweetBox.addEventListener("input", OnInput, false);
    tweetBox.addEventListener("input", changeSubmit, false)
}

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

    console.log("window loaded!!!!!!!")
    if (editModalTrigger) {
        console.log("inside")
        editModalTrigger.onclick = ev => {
            $('#editModal').modal("show");
        }
    }
    if (editCloseBTN) {
        editCloseBTN.onclick = ev => {
            $('#editModal').modal("hide");
        }
    }

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


// $(document).ready(function () {
//
//
// });

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

        // // console.log("next-state: ",);
        // if (btn_state === "Like") {
        //     // this.innerHTML = "Dislike";
        //     btn.setAttribute("next-state", "Dislike");
        // } else {
        //     // this.innerHTML = "Like";
        //     btn.setAttribute("next-state", "Like");
        // }

        event.preventDefault();
        let form = $(this).closest("form");
        console.log('hey there');
        console.log("form", form);


        $.ajax({
            url: form.attr("change-data-url"),
            data: {
                'btn_value': $(this).val(),
                // 'btn_text': btn.getAttribute("next-state"),
            },
            dataType: 'json',
            success: function (data) {

                let btn_state = btn.getAttribute("next-state");
                let query = 'like_cnt' + btn.value;
                let likeCntElem = document.getElementById(query);

                let likeQuery = 'like_img' + btn.value;
                let like_img = document.getElementById(likeQuery);
                console.log('like elem', like_img);

                let dislikeQuery = 'dislike_img' + btn.value;
                let dislike_img = document.getElementById(dislikeQuery);

                if (data.is_liked) {
                    console.log("button value has been changed");
                    // $('.like_img').addClass('d-none');
                    // $('.dislike_img').removeClass('d-none');

                    like_img.classList.add('d-none');
                    dislike_img.classList.remove('d-none');

                    updateLikeCount(likeCntElem, 1);

                    // if (btn_state == "Like")
                    //     btn.classList.add("invisible");
                    // else
                    //     btn.classList.remove("invisible");

                } else {
                    // $('.dislike_img').addClass('d-none');
                    // $('.like_img').removeClass('d-none');

                    dislike_img.classList.add('d-none');
                    like_img.classList.remove('d-none');

                    updateLikeCount(likeCntElem, -1);
                    // if (btn_state == "Dislike")
                    //     btn.classList.add("invisible");
                    // else
                    //     btn.classList.remove("invisible");


                }
            }
        });
    }
}

function updateLikeCount(elem, addedValue) {
    console.log(elem);
    let newValue = parseInt(elem.innerHTML) + addedValue;
    console.log('new value: ', newValue);
    elem.innerHTML = newValue;
}