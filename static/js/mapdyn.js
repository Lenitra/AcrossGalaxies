function move(){
    let a = document.querySelector(".map").offsetHeight;
    console.log(a);

    let lesplans = document.querySelectorAll(".map img:not(.flag)");
    for(let i = 0; i < lesplans.length; i++){

        lesplans[i].style.animation = "float " + (Math.random()+1*5) + "s ease-in-out infinite";
    }
}



