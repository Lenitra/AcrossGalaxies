document.getElementById("statsbtn").addEventListener("click", function() {
    hideall();
    document.getElementById("stats").style.display = "block"; 
});

document.getElementById("logsbtn").addEventListener("click", function() {
    hideall();
    document.getElementById("logs").style.display = "block";
});

document.getElementById("optionsbtn").addEventListener("click", function() {
    hideall();
    document.getElementById("options").style.display = "block";
});

document.getElementById("membresbtn").addEventListener("click", function() {
    hideall();
    document.getElementById("membres").style.display = "block";
});

document.getElementById("changelogbtn").addEventListener("click", function() {
    hideall();
    document.getElementById("changelog").style.display = "block";
});



function hideall() {
    document.getElementById("stats").style.display = "none"; 
    document.getElementById("logs").style.display = "none"; 
    document.getElementById("options").style.display = "none"; 
    document.getElementById("options").style.display = "none"; 
    document.getElementById("changelog").style.display = "none"; 
}

hideall();

document.getElementById("stats").style.display = "block"; 