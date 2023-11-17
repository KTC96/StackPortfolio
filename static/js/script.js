//@ts-check
import { runSignupStepper } from "./stepperForm.js";
import { validateInput, generateErrorSpan } from "./formValidation.js";

// Run functions when the DOM loads
document.addEventListener("DOMContentLoaded", () => {
  handleDeleteButton();
  displayToasts();
  runSlider();

  if (window.location.href.indexOf("signup") > -1) {
    runSignupStepper();
  } else if (
    window.location.href.indexOf("project/create") > -1 ||
    (window.location.href.indexOf("project/") > -1 &&
      window.location.href.indexOf("edit") > -1)
  ) {
    handleProjectForm();
  } else if (
    window.location.href.indexOf("user/") > -1 &&
    window.location.href.indexOf("edit") > -1
  ) {
    handleUserForm();
  }
});

/**
 * Function that displays the toast message on load
 * and then removes it after 3 seconds.
 * @returns {void}
 */
const displayToasts = () => {
  // Check if there are any toast messages
  if (!document.querySelector(".toast")) return;

  // Get all the toast messages
  const toasts = [...document.querySelectorAll(".toast")];

  // Loop through the toast messages and remove
  // them after 3 seconds
  for (const toast of toasts) {
    setTimeout(() => {
      toast.classList.add("opacity-0");
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }
};

/**
 * Check for delete profile button and add
 * event listener to display modal
 * @returns {void}
 */
const handleDeleteButton = () => {
  if (!document.querySelector(".delete-link")) return;
  const deleteProfileButton = document.querySelector(".delete-link");
  const deleteProfileModal = document.getElementById("delete-modal");
  const deleteUserForm = document.querySelector(".delete-form");
  const deleteProfileConfirmButton = document.querySelector(
    ".delete-confirm-button"
  );
  const deleteProfileCancelButton = document.querySelector(
    ".delete-cancel-button"
  );

  if (deleteProfileButton && deleteProfileModal) {
    deleteProfileButton.addEventListener("click", (event) => {
      console.log("clicked");
      event.preventDefault();
      // @ts-ignore
      deleteProfileModal.showModal();
    });
  }
  if (deleteProfileConfirmButton && deleteUserForm) {
    deleteProfileConfirmButton.addEventListener("click", () => {
      if (deleteUserForm instanceof HTMLFormElement) {
        deleteUserForm.submit();
      }
    });
  }

  if (deleteProfileCancelButton && deleteProfileModal) {
    deleteProfileCancelButton.addEventListener("click", (event) => {
      event.preventDefault();
      // @ts-ignore
      deleteProfileModal.close();
    });
  }
};

/**
 * Hanlde profile creation and edit forms
 * @returns {void}
 */

const handleProjectForm = () => {
  const projectFormInputs = [
    ...document.querySelectorAll(
      "input:not([type='checkbox']):not([type='radio']):not([type='file']):not([type='hidden']:not([name='tech_input']), textarea"
    ),
  ];
  const submitButton = document.querySelector("button[type='submit']");

  for (const input of projectFormInputs) {
    input.addEventListener("input", () => {
      if (input instanceof HTMLInputElement) {
        input.dataset.touched = "true";
        if (input.name == "name") {
          validateInput({
            input,
            customMinLength: 3,
            customPattern: "^(?=.*[A-Za-z])[A-Za-z\\d\\s]{3,100}$",
            customValidationMessage:
              "Project name must be at least 3 characters long and can't contain symbols.",
          });
        } else {
          validateInput({ input });
        }
      }
      checkAllInputs();
    });
  }

  const checkAllInputs = () => {
    // @ts-ignore
    if (projectFormInputs.every((input) => input.checkValidity())) {
      if (submitButton instanceof HTMLButtonElement) {
        submitButton.disabled = false;
        submitButton.ariaDisabled = "false";
        submitButton.classList.remove("opacity-50", "cursor-not-allowed");
      }
    } else {
      if (submitButton instanceof HTMLButtonElement) {
        submitButton.disabled = true;
        submitButton.ariaDisabled = "true";
        submitButton.classList.add("opacity-50", "cursor-not-allowed");
      }
    }
  };
  checkAllInputs();
};

/**
 * Run slider on the home page
 * Adapted from kindacode:
 * https://www.kindacode.com/article/tailwind-css-create-an-image-carousel-slideshow/
 * @returns {void}
 */

const runSlider = () => {
  let slideIndex = 1;
  const slides = document.querySelectorAll(".slide");
  const dots = document.querySelectorAll(".dot");

  const prevButton = document.querySelector(".carousel-prev");
  const nextButton = document.querySelector(".carousel-next");

  if (!prevButton || !nextButton) {
    return;
  } else {
    prevButton.addEventListener("click", () => moveSlide(-1));
    nextButton.addEventListener("click", () => moveSlide(1));
  }

  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => currentSlide(index + 1));
  });

  function moveSlide(moveStep) {
    showSlide((slideIndex += moveStep));
  }

  function currentSlide(index) {
    showSlide((slideIndex = index));
  }

  function showSlide(index) {
    if (index > slides.length) {
      slideIndex = 1;
    }
    if (index < 1) {
      slideIndex = slides.length;
    }

    slides.forEach((slide) => slide.classList.add("hidden"));
    dots.forEach((dot) => dot.classList.replace("bg-primary", "bg-secondary"));

    slides[slideIndex - 1].classList.remove("hidden");
    dots[slideIndex - 1].classList.replace("bg-secondary", "bg-primary");
  }

  // Initially show the first slide
  showSlide(slideIndex);
};

/**
 * Handle the user profile edit form
 * @returns {void}
 */
const handleUserForm = () => {
  const userFormInputs = [
    ...document.querySelectorAll(
      "input:not([type='checkbox']):not([type='radio']):not([type='file']):not([type='hidden'], textarea"
    ),
  ];
  const submitButton = document.querySelector("button[type='submit']");

  for (const input of userFormInputs) {
    input.addEventListener("input", () => {
      if (input instanceof HTMLInputElement) {
        input.dataset.touched = "true";
        if (input.name === "first_name" || input.name === "last_name") {
          validateInput({
            input,
            customMaxLength: 40,
            customRequired: true,
          });
        } else if (input.type === "tel") {
          validateInput({
            input,
            customValidationMessage:
              "Phone numbers can only be numbers and be between 10 and 15 characters long.",
          });
        } else if (input.name === "username") {
          validateInput({
            input,
            customMaxLength: 20,
            customValidationMessage:
              "Username must contain 5 characters and it can't contain symbols or spaces.",
          });
        }
        validateInput({ input });
      }
      checkAllInputs();
    });
  }

  const checkAllInputs = () => {
    // @ts-ignore
    if (userFormInputs.every((input) => input.checkValidity())) {
      if (submitButton instanceof HTMLButtonElement) {
        submitButton.disabled = false;
        submitButton.ariaDisabled = "false";
        submitButton.classList.remove("opacity-50", "cursor-not-allowed");
      }
    } else {
      if (submitButton instanceof HTMLButtonElement) {
        submitButton.disabled = true;
        submitButton.ariaDisabled = "true";
        submitButton.classList.add("opacity-50", "cursor-not-allowed");
      }
    }
  };
  checkAllInputs();
};
