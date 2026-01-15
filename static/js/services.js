// FILTERING
const filterButtons = document.querySelectorAll(".filter-btn");
const cards = document.querySelectorAll(".service-card");
var filter = "all"


filterButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    filterButtons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    filter = btn.dataset.filter;
	searchBar.value='';
	

    cards.forEach(card => {
      if (filter === "all" || card.dataset.category === filter) {
        card.classList.remove('hidden');
      } else {
        card.classList.add('hidden');
      }
    });
  });
});

function filterSuggestions() {
const searchTerm = document.getElementById('searchBar').value.toLowerCase();
const noResults = document.getElementById('noResults');

let visibleCount = 0;

cards.forEach(card => {
                const text = card.textContent.toLowerCase();

                const matchesSearch = text.includes(searchTerm);
				
				console.log(filter);
				console.log("a");

                if (matchesSearch) {
					if (filter === "all" || card.dataset.category === filter) {
                    card.classList.remove('hidden');
                    visibleCount++;
					}
					else{
					card.classList.add('hidden');
					}
                } else {
                    card.classList.add('hidden');
                }
            });
			
			            // Show/hide no results message
            if (visibleCount === 0) {
                noResults.classList.remove('hidden');
            } else {
                noResults.classList.add('hidden');
            }
}


// READ MORE
document.querySelectorAll(".read-more").forEach(btn => {
  btn.addEventListener("click", () => {
    const more = btn.nextElementSibling;
    const open = more.style.display === "block";
    more.style.display = open ? "none" : "block";
    btn.textContent = open ? "READ MORE" : "READ LESS";
  });
});

// LOAD MORE (demo)
document.getElementById("loadMore").addEventListener("click", () => {
  alert("Load more would fetch more services from backend.");
});