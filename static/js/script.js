//@ts-check
import { runSignupStepper } from "./stepperForm.js";
import { validateInput, generateErrorSpan } from "./formValidation.js";

// Run functions when the DOM loads
document.addEventListener("DOMContentLoaded", () => {
  handleDeleteProfileButton();
  displayToasts();

  if (window.location.href.indexOf("signup") > -1) {
    runSignupStepper();
  } else if (
    window.location.href.indexOf("project/create") > -1 ||
    window.location.href.indexOf("project/edit") > -1
  ) {
    handleProjectForm();
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
const handleDeleteProfileButton = () => {
  if (!document.querySelector(".delete-profile-link")) return;
  const deleteProfileButton = document.querySelector(".delete-profile-link");
  const deleteProfileModal = document.getElementById("delete-profile-modal");
  const deleteUserForm = document.querySelector(".delete-user-form");
  const deleteProfileConfirmButton = document.querySelector(
    ".delete-user-confirm-button"
  );
  const deleteProfileCancelButton = document.querySelector(
    ".delete-user-cancel-button"
  );

  if (deleteProfileButton && deleteProfileModal) {
    deleteProfileButton.addEventListener("click", (event) => {
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
        if (input.name == "project_name") {
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
