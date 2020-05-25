const nav_toggler = document.getElementById("nav-toggler");

nav_toggler.addEventListener("click", function(){
    const content = nav_toggler.getAttribute("data-target");
    document.getElementById(content).classList.toggle("open");
})