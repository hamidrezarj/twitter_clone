
console.log("Hello world.");

let likeBtns = document.getElementsByClassName('like_btn');
console.log(likeBtns);
for(let btn of likeBtns){

    btn.onclick = function (event) {
        if(this.innerHTML === "Like")
            this.innerHTML = "Dislike";
        else
            this.innerHTML = "Like";

        event.preventDefault();
    }
}