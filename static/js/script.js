// Navbar dropdown    
{
    document.addEventListener("click", function (e) {
        const dropdown = document.querySelector(".profile-dropdown");
        dropdown.classList.toggle("active", dropdown.contains(e.target));
    });
}

// Watchlist toggle - Index Page
{
    function toggleWatchlist_index(btn) {
        btn.classList.toggle("active");
            
        const text = btn.querySelector(".text");
            
        text.textContent = btn.classList.contains("active")
        ? "✔ Added to Watchlist"
        : "+ Add to Watchlist";
    }
}

// Like, Watched and Watchlist toggles - Movie Detail Page
{
    function toggleLike(btn){
        btn.classList.toggle("active");
        const icon = btn.querySelector(".icon");
        const text = btn.querySelector(".text");
        if(btn.classList.contains("active")){
            icon.textContent="♥"; text.textContent="Liked";
        }else{
            icon.textContent="♡"; text.textContent="Like";
        }
    }

    function toggleWatched(btn){
        btn.classList.toggle("active");
        const text = btn.querySelector(".text");
        text.textContent = btn.classList.contains("active") ? "Watched":"Watch";
    }

    function toggleWatchlist(btn){
        btn.classList.toggle("active");
        const text = btn.querySelector(".text");
        text.textContent = btn.classList.contains("active") ? "Watchlisted":"Watchlist";
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