/* =========================================
   OTT EXPLORER JAVASCRIPT
   Stable Version (Flask Safe)
========================================= */


/* =========================================
   IMAGE FALLBACK
========================================= */

document.addEventListener("DOMContentLoaded", function(){

    const images = document.querySelectorAll("img");

    images.forEach(function(img){

        img.onerror = function(){

            this.src = "https://via.placeholder.com/300x450?text=No+Poster";

        };

    });

});


/* =========================================
   POSTER HOVER EFFECT
========================================= */

document.addEventListener("DOMContentLoaded", function(){

    const posters = document.querySelectorAll(".poster");

    posters.forEach(function(poster){

        poster.addEventListener("mouseenter", function(){

            poster.style.transform = "scale(1.08)";
            poster.style.transition = "0.25s ease";
            poster.style.boxShadow = "0 10px 25px rgba(0,0,0,0.7)";

        });

        poster.addEventListener("mouseleave", function(){

            poster.style.transform = "scale(1)";
            poster.style.boxShadow = "none";

        });

    });

});


/* =========================================
   POSTER CLICK ANIMATION
========================================= */

document.addEventListener("DOMContentLoaded", function(){

    const posters = document.querySelectorAll(".poster");

    posters.forEach(function(poster){

        poster.addEventListener("click", function(){

            poster.style.transform = "scale(0.95)";

            setTimeout(function(){

                poster.style.transform = "scale(1)";

            },150);

        });

    });

});


/* =========================================
   ANIME CARD HOVER
========================================= */

document.addEventListener("DOMContentLoaded", function(){

    const animeCards = document.querySelectorAll(".anime-card");

    animeCards.forEach(function(card){

        card.addEventListener("mouseenter", function(){

            card.style.transform = "scale(1.08)";
            card.style.transition = "0.25s ease";
            card.style.zIndex = "10";
            card.style.boxShadow = "0 10px 30px rgba(0,0,0,0.8)";

        });

        card.addEventListener("mouseleave", function(){

            card.style.transform = "scale(1)";
            card.style.zIndex = "1";
            card.style.boxShadow = "none";

        });

    });

});


/* =========================================
   SEARCH HIGHLIGHT (Frontend assist)
   Does not block Flask search
========================================= */

function searchMovies(){

    const input = document.getElementById("searchInput");

    if(!input) return;

    const filter = input.value.toLowerCase();

    const cards = document.querySelectorAll(".card");

    cards.forEach(function(card){

        const text = card.innerText.toLowerCase();

        if(text.includes(filter)){

            card.style.opacity = "1";
            card.style.transform = "scale(1.03)";

        }
        else{

            card.style.opacity = "0.4";
            card.style.transform = "scale(1)";

        }

    });

}


/* =========================================
   TRAILER MODAL
========================================= */

function openTrailer(videoKey){

    const modal = document.getElementById("trailerModal");
    const frame = document.getElementById("trailerFrame");

    if(!modal || !frame) return;

    frame.src = "https://www.youtube.com/embed/" + videoKey;

    modal.style.display = "flex";

}


function closeTrailer(){

    const modal = document.getElementById("trailerModal");
    const frame = document.getElementById("trailerFrame");

    if(!modal || !frame) return;

    frame.src = "";

    modal.style.display = "none";

}


/* =========================================
   CONTINUE WATCHING STORAGE
========================================= */

function saveContinueWatching(movieId, time){

    try{

        localStorage.setItem("movie_" + movieId, time);

    }
    catch(e){

        console.log("Storage error");

    }

}


function getContinueWatching(movieId){

    try{

        return localStorage.getItem("movie_" + movieId);

    }
    catch(e){

        return null;

    }

}


/* =========================================
   PAGE LOADER
========================================= */

window.onload = function(){

    const loader = document.getElementById("loader");

    if(loader){

        loader.style.opacity = "0";

        setTimeout(function(){

            loader.style.display = "none";

        },300);

    }

};


/* =========================================
   KEYBOARD NAVIGATION
========================================= */

document.addEventListener("keydown", function(e){

    if(e.key === "ArrowRight"){

        window.scrollBy({
            left:350,
            behavior:"smooth"
        });

    }

    if(e.key === "ArrowLeft"){

        window.scrollBy({
            left:-350,
            behavior:"smooth"
        });

    }

});


/* =========================================
   MOBILE MENU
========================================= */

function toggleMenu(){

    const menu = document.getElementById("mobileMenu");

    if(!menu) return;

    if(menu.style.display === "block"){

        menu.style.display = "none";

    }
    else{

        menu.style.display = "block";

    }

}


/* =========================================
   SCROLL TO TOP BUTTON
========================================= */

window.addEventListener("scroll", function(){

    const btn = document.getElementById("scrollTop");

    if(!btn) return;

    if(window.scrollY > 500){

        btn.style.display = "block";

    }
    else{

        btn.style.display = "none";

    }

});


function scrollTopPage(){

    window.scrollTo({
        top:0,
        behavior:"smooth"
    });

}