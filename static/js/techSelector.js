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

  submitButton.addEventListener("click", (e) => {
    e.preventDefault();
  });
});
