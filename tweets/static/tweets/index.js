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
    if (!validateTweetBox()) { // IMPORTANT: AND IF IMG WAS EMPTY
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

var file = document.getElementById("imgFile");
console.log(file)
let loadFile = function (event) {
    let output = document.getElementById("uploadImgContainer");
    let src = URL.createObjectURL(file.files[0]);
    output.innerHTML = "";
    console.log("inside baby")

    var e = document.createElement('div');
    e.innerHTML = "<img src='" + src + "' alt='Image' class='tweetImg'></div>";
    console.log(e.innerHTML)
    while (e.firstChild) {
        output.appendChild(e.firstChild);
    }

};
if (file) {
    file.onchange = loadFile;
}


var pfpfile = document.getElementById("pfpImgFile");
console.log(pfpfile)
let loadFilePfp = function (event) {
    let output = document.getElementById("pfpImgContainer");
    let src = URL.createObjectURL(pfpfile.files[0]);
    output.innerHTML = "";
    console.log("inside baby");

    var e = document.createElement('div');
    e.innerHTML = "<img src='" + src + "' id='pfpImgContainer2' alt='Image' class='tweetImg rounded-circle'></div>";
    console.log(e.innerHTML)
    while (e.firstChild) {
        output.appendChild(e.firstChild);
    }

};
if (pfpfile) {
    pfpfile.onchange = loadFilePfp;
}


var myModal = document.getElementById('exampleModal');
var myInput = document.getElementById('exampleTrigger');
var mycloseBTN = document.getElementById('closeBTN');


// var editModal = document.getElementById('editModal');
var editModalTrigger = document.getElementById('editTrigger');
var editCloseBTN = document.getElementById('editCloseBTN');

// var followingModal = document.getElementById('followingModal');
var followingModalTrigger = document.getElementById('followingTrigger');
var followingCloseBTN = document.getElementById('followingCloseBTN');

// var followersModal = document.getElementById('followersModal');
var followersModalTrigger = document.getElementById('followersTrigger');
var followersCloseBTN = document.getElementById('followersCloseBTN');

// var likesModal = document.getElementById('likesModal');
var likesModalTrigger = document.getElementById('likesTrigger');
var likesCloseBTN = document.getElementById('likesCloseBTN');
window.addEventListener('load', (event) => {
    // console.log("Listeners Added");
    // $(document).ready(function(){
    //     $('#likesModal').modal("show");
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

    if (followingModalTrigger) {
        followingModalTrigger.onclick = ev => {
            $('#followingModal').modal("show");
        }
    }
    if (followingCloseBTN) {
        followingCloseBTN.onclick = ev => {
            $('#followingModal').modal("hide");
        }
    }

    if (followersModalTrigger) {
        followersModalTrigger.onclick = ev => {
            $('#followersModal').modal("show");
        }
    }
    if (followersCloseBTN) {
        followersCloseBTN.onclick = ev => {
            $('#followersModal').modal("hide");
        }
    }

    if (likesModalTrigger) {
        likesModalTrigger.onclick = ev => {
            $('#likesModal').modal("show");
        }
    }
    if (likesCloseBTN) {
        likesCloseBTN.onclick = ev => {
            $('#likesModal').modal("hide");
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

    //search bar
    $("#searchTxt1").change(function (event) {
        event.preventDefault();
        if (event.keyCode === 13) {
            console.log('ENTER KEY');
            if ($(this).val() != "") {
                $(this).closest('form').submit();
            }

        }
    });

    $("#likesTrigger").click(function (event) {
        event.preventDefault();

        let url_ = $(this).attr("show-data-url");

        $.ajax({
            url: url_,
            data: {},
            success: function (data) {
                // var likes = JSON.parse(data.likes);
                // console.log(likes);
                // for (let like_obj of likes) {
                //     console.log(like_obj.fields.profile_img);
                //     console.log(like_obj.fields.user);
                //     console.log(like_obj.fields);
                // }

                var like_usernames = data.like_usernames;
                var profile_images = data.profile_images;
                console.log(like_usernames);
                console.log(profile_images);

                var like_container = document.getElementById('likeListContainer');

                let output = document.getElementById("likeListContainer");
                output.innerHTML = "";
                console.log("inside baby")


                for (let i = 0; i < like_usernames.length; i++) {
                    console.log("i: " +i)
                        // <hr class='my-2 lineBreak' style='width: 100%; background-color: white; margin:-1px 0;'>
                        //
                        // <div class='pfpSmolContainer d-inline-block px-0 mt-3 mx-2'
                        //      style='min-height: 100%; vertical-align:top'>
                        //     <a href='{% url 'tweets:profile' user.username %}'>
                        //         <img class='rounded pfpSmol'
                        //              src='https://mdbootstrap.com/img/Photos/Others/placeholder-avatar.jpg'
                        //              style='border: 2px solid #51D2B7;'/>
                        //
                        //     </a>
                        // </div>
                        // <div class='pfpPopupOffset d-inline-block px-0 mr-0 mb-2'>
                        //     <div class='align-items-center pt-3'>
                        //         <b class='text thirdColumnTxt'>THIS USER IS FOLLOWING: USERNAME</b>
                        //         <div class='justify-self-end ml-auto'>
                        //             <button class='btn btn-info'>
                        //                 Follow
                        //             </button>
                        //         </div>
                        //     </div>
                        // </div>


                var e = document.createElement('div');
                e.className += "d-inline-block";
                e.innerHTML =
                    "                        <hr class='my-2 lineBreak' style='width: 100%; background-color: white; margin:-1px 0;'>" +
                    "                        <div class='pfpSmolContainer d-inline-block px-0 mt-3 mx-2'" +
                    "                             style='min-height: 100%; vertical-align:top'>" +
                    "                            <a href='{% url 'tweets:profile' " + like_usernames[i] + " %}'>" +
                    "                                <img class='rounded pfpSmol' " +
                    "                                     src='" + profile_images[i]  + "'" +
                    "                                     style='border: 2px solid #51D2B7;'/>" +
                    "                            </a>" +
                    "                        </div>" +
                console.log(e.innerHTML)
                e.innerHTML +=
                    "                        <div class='pfpPopupOffset d-inline-block px-0 mr-0 mb-2'>" +
                    "                            <div class='align-items-center pt-3'>" +
                    "                                <b class='text thirdColumnTxt'>" + like_usernames[i] +"</b>" +
                    "                                <div class='justify-self-end ml-auto'>" +
                    "                                    <button class='btn btn-info'>" +
                    "                                        Follow" +
                    "                                    </button>" +
                    "                                </div>" +
                    "                            </div>" +
                    "                        </div>"
                output.appendChild(e);

                }


                // var likes = JSON.parse('{{data|safe}}');
                // console.log(likes);
            }, error: function () {

            }
        })

    })
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

var retweetBtns = document.getElementsByClassName('retweet_btns');

for (let retBtn of retweetBtns) {

    retBtn.onclick = function (event) {
        console.log('clicked on ret');
        event.preventDefault();
        let url_ = $(this).attr('change-data-url');
        console.log(url_);

        $.ajax({
            url: url_,
            data: {
                'btn_value': $(this).val()
            },
            success: function (data) {
                // let svgElem = $(this).find('svg');
                // console.log('svg: ', svgElem);
                if (data.is_retweeted) {
                    console.log('retweeted successfullly');
                    //add class retweet button
                    retBtn.classList.add('retweeted');


                } else {
                    retBtn.classList.remove('retweeted');
                }

            },
            error: function (error) {
                console.log('error: ', error)
            }
        })
    }
}

var deleted_btns = document.getElementsByClassName('delete_btns');

for (let del_btn of deleted_btns) {
    del_btn.onclick = function (event) {
        event.preventDefault();
        console.log(window.location);
        $.ajax({
            url: $(this).attr('change-data-url'),
            data: {},
            success: function (data) {
                // window.location.replace('/')
                if (!data.error)
                    window.location.reload();
            }, error() {

            }
        })
    }
}

