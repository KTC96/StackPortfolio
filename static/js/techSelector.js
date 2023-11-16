document.addEventListener("DOMContentLoaded", () => {
  // select the dom elements I need to work with
  const techInput = document.querySelector(".tech-input");
  const techDropdown = document.querySelector(".tech-dropdown");
  const techList = document.querySelector(".tech-list");
  const techListItems = [...document.querySelectorAll("li.tech-list__item")];
  const addedTechContainer = document.querySelector(".added-tech-container"); // contain on the frontend
  const selectedTechContainer = document.getElementById("selectedTechnologies"); // input field to send tech to backend
  const form = document.querySelector("form");
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

  /**
   * Updates the focus state of the list items based on the focusedListItemIndex
   * variable. This runs when the user is on the tech input field and presses the
   * up or down arrow keys, and if the list is visible.
   *
   * @returns {void}
   */
  const updateListItemFocus = () => {
    const visibleItems = techListItems.filter(
      (item) => !item.classList.contains("hidden")
    );
    for (const [index, item] of visibleItems.entries()) {
      item.classList.toggle("bg-primary", index === focusedListItemIndex);
      item.classList.toggle("text-white", index === focusedListItemIndex);
    }
  };

  /**
   * Get the ID from the tech name.
   * If there's an id, use that, otherwise return null.
   * @param {string} techName The name of the tech
   * @returns {number|null} The ID of the tech, or null if not found
   *
   */
  const getTechIdByName = (techName) => {
    const tech = allActiveTech.find((tech) => tech.name === techName);
    return tech ? tech.id : null;
  };

  /**
   * Updates the hidden input fields that are sent to the backend
   * with the selected tech. This runs whenever a tech is added or
   * removed from the list.
   * @returns {void}
   * */
  const updateHiddenTechInputs = () => {
    // Clear existing inputs
    selectedTechContainer.innerHTML = "";
    let newTechInputValue = "";

    for (const techName of selectedTech) {
      const techId = getTechIdByName(techName);
      if (techId) {
        // If it's an existing tech, create a hidden input with the tech ID
        const input = document.createElement("input");
        input.type = "hidden";
        input.name = "technologies"; // "technologies" field is what backend expects
        input.value = techId;
        selectedTechContainer.appendChild(input);
      } else {
        // If it's a new tech, add it to the newTechInputValue string
        newTechInputValue += techName + ",";
      }
    }

    // Create a hidden input for new technologies
    const newTechInput = document.createElement("input");
    newTechInput.type = "hidden";
    newTechInput.name = "new_technologies"; // A separate field for new tech
    newTechInput.value = newTechInputValue;
    selectedTechContainer.appendChild(newTechInput);
  };

  // if addedTechContainer has children, add them to the selectedTech array
  if (addedTechContainer.children.length > 0) {
    for (const child of addedTechContainer.children) {
      selectedTech.push(child.querySelector(".added-tech strong").textContent);
    }

    // update the hidden inputs
    updateHiddenTechInputs();
  }

  /**
   * Creates the HTML for the added tech button, including
   * the little `x` svg icon.
   * @param {string} techName The name of the tech to add
   * @param {boolean} isCustom Whether the tech is in the list or not
   * @returns {HTMLElement} The HTML button element
   */
  const addedTechHtml = (techName, isCustom) => {
    const button = document.createElement("button");
    const buttonContent = document.createElement("div");
    const techNameContainer = document.createElement("div");
    const strongElement = document.createElement("strong");
    const svgNS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(svgNS, "svg");
    const line1 = document.createElement("line");
    const line2 = document.createElement("line");

    // need to set the type to prevent form validation
    // from triggering when the button is clicked
    button.setAttribute("type", "button");

    button.classList.add("group", "added-tech-button");
    buttonContent.classList.add(
      "flex",
      "justify-center",
      "text-primary",
      "items-center",
      "mr-1",
      "py-2",
      "px-5",
      "rounded-md",
      "bg-aliceblue",
      "bordered",
      "border-neutral",
      "text-neutral",
      "bg-white",
      "border-primary",
      "border-2",
      "group-hover:border-secondary"
    );
    techNameContainer.classList.add(
      "group-hover:text-secondary",
      "cursor-pointer",
      "text-sm",
      "font-normal",
      "flex-initial",
      "added-tech"
    );

    svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    svg.setAttribute("width", "3");
    svg.setAttribute("height", "3");
    svg.setAttribute("fill", "none");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("stroke", "currentColor");

    svg.setAttributeNS(null, "width", "3");
    svg.setAttributeNS(null, "height", "3");
    svg.setAttributeNS(null, "viewBox", "0 0 24 24");
    svg.setAttributeNS(null, "fill", "none");
    svg.setAttributeNS(null, "stroke", "currentColor");

    const createLine = (x1, y1, x2, y2) => {
      const line = document.createElementNS(svgNS, "line");
      line.setAttributeNS(null, "x1", x1);
      line.setAttributeNS(null, "y1", y1);
      line.setAttributeNS(null, "x2", x2);
      line.setAttributeNS(null, "y2", y2);
      return line;
    };
    svg.classList.add(
      "feather",
      "feather-x",
      "text-primary",
      "text-neutral",
      "group-hover:text-secondary",
      "rounded-full",
      "w-3",
      "h-3",
      "ml-2"
    );

    if (!isCustom) {
      buttonContent.classList.remove(
        "text-neutral",
        "border-neutral",
        "bg-white"
      );

      svg.classList.remove("text-neutral");
    } else {
      buttonContent.classList.remove(
        "border-primary",
        "bg-aliceblue",
        "text-primary"
      );
      svg.classList.remove("text-primary");
    }

    svg.appendChild(createLine("18", "6", "6", "18"));
    svg.appendChild(createLine("6", "6", "18", "18"));

    strongElement.textContent = techName;
    techNameContainer.appendChild(strongElement);
    buttonContent.appendChild(techNameContainer);
    button.appendChild(buttonContent);
    svg.appendChild(line1);
    svg.appendChild(line2);
    buttonContent.appendChild(svg);

    return button;
  };

  /**
   * Adds a tech to the selected tech list and updates the hidden inputs
   * fields to send to the backend.
   * @param {string} techName The name of the tech to add
   * @returns {void}
   */
  const addTechToSelected = (techName) => {
    // Check if the tech name matches an existing tech name (ignoring case)
    // so that different case names don't get added
    const existingTech = allActiveTech.find(
      (tech) => tech.name.toLowerCase() === techName.toLowerCase()
    );
    const finalTechName = existingTech ? existingTech.name : techName;

    // Determine if the tech is custom or existing
    const isCustom = !existingTech;

    if (!selectedTech.includes(finalTechName)) {
      selectedTech.push(finalTechName);
      addedTechContainer.append(addedTechHtml(finalTechName, isCustom));
      updateHiddenTechInputs();

      techInput.value = "";
      techDropdown.classList.add("hidden");
    }

    // refocus on the input for a better user experience
    techInput.focus();
  };

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

  techInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      const inputValue = techInput.value.trim();
      const visibleItems = techListItems.filter(
        (item) => !item.classList.contains("hidden")
      );

      if (visibleItems.length > 0 && focusedListItemIndex !== -1) {
        addTechToSelected(
          visibleItems[focusedListItemIndex].textContent.trim()
        );
        focusedListItemIndex = -1; // Reset the focused item index
      } else if (inputValue) {
        addTechToSelected(inputValue, true);
      }
      techInput.value = ""; // Clear the input field
      techDropdown.classList.add("hidden"); // Hide the dropdown again
      dropdownVisible = false;
      return; // Return early to avoid other key events happening
    }

    if (!dropdownVisible) return;

    // filter out items that aren't visible
    const visibleItems = techListItems.filter(
      (item) => !item.classList.contains("hidden")
    );

    const visibleItemsCount = visibleItems.length;

    // add functionality to up and down arrows to navigate the list
    if (e.key === "ArrowDown") {
      e.preventDefault();
      focusedListItemIndex = (focusedListItemIndex + 1) % visibleItemsCount;
      updateListItemFocus();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      if (focusedListItemIndex <= 0) focusedListItemIndex = visibleItemsCount;
      focusedListItemIndex = (focusedListItemIndex - 1) % visibleItemsCount;
      updateListItemFocus();
    }
  });

  techList.addEventListener("click", (e) => {
    const listItem = e.target.closest(".tech-list__item");
    if (listItem) {
      addTechToSelected(listItem.textContent.trim());
    }

    listItem.classList.toggle(
      "hidden",
      selectedTech.includes(listItem.textContent.trim())
    );
  });

  addedTechContainer.addEventListener("click", (e) => {
    const techButton = e.target.closest(".added-tech-button");
    if (techButton) {
      const techName = techButton
        .querySelector(".added-tech strong")
        .textContent.trim();
      const index = selectedTech.indexOf(techName);
      if (index !== -1) {
        selectedTech.splice(index, 1);
        techButton.remove();
        updateHiddenTechInputs();
      }
    }
  });

  submitButton.addEventListener("click", (e) => {
    e.preventDefault();
    updateHiddenTechInputs();
    form.submit();
  });
});
