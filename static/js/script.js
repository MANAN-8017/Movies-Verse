// Navbar dropdown    
// {
//     document.addEventListener("click", function (e) {
//         const dropdown = document.querySelector(".profile-dropdown");
//         dropdown.classList.toggle("active", dropdown.contains(e.target));
//     });
// }
document.addEventListener("click", function (e) {
    const dropdown = document.querySelector(".profile-dropdown");
    if(dropdown){
        dropdown.classList.toggle("active", dropdown.contains(e.target));
    }
});


function toggleWatchlist_index(btn, imdbId){

    fetch(`/watchlist/toggle/${imdbId}/`)
    .then(res => res.json())
    .then(data => {

        const text = btn.querySelector(".text");

        if(data.status === "added"){
            btn.classList.add("active");
            text.innerHTML = "✔ Added to Watchlist";
        }

        if(data.status === "removed"){
            btn.classList.remove("active");
            text.innerHTML = "+ Add to Watchlist";
        }

    });

}

function toggleWatchlist_detail(btn){

    // get imdb id from button
    const imdbId = btn.dataset.imdb;

    if(!imdbId){
        console.error("IMDb ID missing!");
        return;
    }

    fetch(`/watchlist/toggle/${imdbId}/`)
    .then(response => response.json())
    .then(data => {

        const text = btn.querySelector(".text");

        if(data.status === "added"){
            btn.classList.add("active");
            text.innerHTML = "Watchlisted";
        }

        if(data.status === "removed"){
            btn.classList.remove("active");
            text.innerHTML = "Watchlist";
        }

    }).catch(error => {
        console.error("Watchlist toggle error:", error);
    });

}


// Like, Watched and Watchlist toggles - Movie Detail Page
{
    

    function toggleLike(btn){

        const imdbId = btn.dataset.imdb;
    
        if(!imdbId){
            console.error("IMDb ID missing!");
            return;
        }
    
        fetch(`/like/toggle/${imdbId}/`)
        .then(res => res.json())
        .then(data => {
    
            const icon = btn.querySelector(".icon");
            const text = btn.querySelector(".text");
    
            if(data.status === "added"){
                btn.classList.add("active");
                icon.textContent = "♥";
                text.textContent = "Liked";
            }
    
            if(data.status === "removed"){
                btn.classList.remove("active");
                icon.textContent = "♡";
                text.textContent = "Like";
            }
    
        });
    
    }

    function toggleWatched(btn){

        const imdbId = btn.dataset.imdb;
    
        if(!imdbId){
            console.error("IMDb ID missing!");
            return;
        }
    
        fetch(`/watched/toggle/${imdbId}/`)
        .then(res => res.json())
        .then(data => {
    
            const text = btn.querySelector(".text");
    
            if(data.status === "added"){
                btn.classList.add("active");
                text.innerHTML = "Watched";
            }
    
            if(data.status === "removed"){
                btn.classList.remove("active");
                text.innerHTML = "Watch";
            }
    
        });
    
    }


    document.addEventListener("DOMContentLoaded",()=>{
        document.querySelectorAll(".stars").forEach(container=>{
            const rating=parseFloat(container.dataset.rating);
            container.innerHTML="";
            for(let i=1;i<=5;i++){
                if(rating>=i) container.innerHTML+='<span class="star filled">★</span>';
                else if(rating>=i-0.5) container.innerHTML+='<span class="star half">★</span>';
                else container.innerHTML+='<span class="star">★</span>';
            }
        });
    });
}

// Accordion toggle - Settings page
{
    function toggleAccordion(btn) {
    const item = btn.closest('.accordion-item');
    const isOpen = item.classList.contains('open');
    btn.closest('.settings-section').querySelectorAll('.accordion-item').forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
    }

    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(el => {
            el.style.opacity = '0';
            setTimeout(() => el.remove(), 300);
        });
    }, 4000);
}