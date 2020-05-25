const audioPlayer = document.getElementById("spotify-preview-audio");
const previews = document.getElementsByClassName("spotify-preview");

audioPlayer.addEventListener("canplaythrough", function() {
    // remove spinner and go to active state
    const src = audioPlayer.getAttribute("src");
    const icon = document.querySelector('i[data-preview-url="' + src + '"]');
    icon.classList.remove("loading");
    icon.classList.remove("fa-spin");
    icon.classList.add("active");
});

audioPlayer.addEventListener("ended", function() {
    // move out of active state
    const src = audioPlayer.getAttribute("src");
    const icon = document.querySelector('i[data-preview-url="' + src + '"]');
    icon.classList.remove("active");
});

for (let i=0; i < previews.length; i++) {
    const preview = previews[i];

    preview.addEventListener("click", function() {
        const new_src  = preview.getAttribute("data-preview-url");
        const prev_src = audioPlayer.getAttribute("src");

        if (prev_src === new_src) {

            if (audioPlayer.classList.contains("active")) {
                audioPlayer.pause();
            } else {
                audioPlayer.play();
            }

            preview.classList.toggle("active");
            audioPlayer.classList.toggle("active");

        } else {
            const oldIcon = document.querySelector('i[data-preview-url="' + prev_src + '"]');
            if (oldIcon) {
                oldIcon.classList.remove("active");
            }
            preview.classList.add("loading");
            preview.classList.add("fa-spin");
            audioPlayer.classList.add("active");

            audioPlayer.setAttribute("src", new_src);
            audioPlayer.load();
            audioPlayer.play();
        }
    });
}
