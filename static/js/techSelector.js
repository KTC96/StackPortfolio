document.addEventListener("DOMContentLoaded", () => {
  // select the dom elements I need to work with
  const techInput = document.querySelector(".tech-input");
  const techDropdown = document.querySelector(".tech-dropdown");
  const techList = document.querySelector(".tech-list");
  const techListItems = [...document.querySelectorAll("li.tech-list__item")];
  const addedTechContainer = document.querySelector(".added-tech-container"); // contain on the frontend
  const selectedTechContainer = document.getElementById("selectedTechnologies"); // input field to send tech to backend
  const form = document.querySelector(".create-project-form");
  const submitButton = document.querySelector("button[type='submit']");
  const selectedTech = [];
  const allActiveTech = [];
  let focusedListItemIndex = -1;
  let dropdownVisible = false;

  // loop though techListItems output on DOM
  // add item and id to the allActiveTech array
  for (const item of techListItems) {
    allActiveTech.push({
      id: item.dataset.techid, // added this to the list item in the html
      name: item.textContent.trim(),
    });
  }

  // prevent form submission when enter is pressed
  form.addEventListener("submit", (e) => {
    e.preventDefault();
  });

  // when a key is pressed in the techInput,
  // display the dropdown - filter out any non-
  // matching items
  techInput.addEventListener("input", (e) => {
    const value = e.target.value.toLowerCase();
    if (value.length > 0) {
      techDropdown.classList.remove("hidden");
    } else {
      techDropdown.classList.add("hidden");
    }
    techListItems.filter((item) => {
      item.textContent.toLowerCase().includes(value) &&
      !selectedTech.includes(item.textContent.trim())
        ? item.classList.remove("hidden")
        : item.classList.add("hidden");
    });
    dropdownVisible = techInput.value.length > 0;
  });

  submitButton.addEventListener("click", (e) => {
    e.preventDefault();
  });
});
