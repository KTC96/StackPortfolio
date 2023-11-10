import { runSignupStepper } from "./formValidation.js";

// Run functions when the DOM loads
document.addEventListener("DOMContentLoaded", () => {
  handleDeleteProfileButton();
  displayToasts();

  if (window.location.href.indexOf("signup") > -1) {
    runSignupStepper();
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

  deleteProfileButton.addEventListener("click", (event) => {
    event.preventDefault();
    deleteProfileModal.showModal();
  });

  deleteProfileConfirmButton.addEventListener("click", () => {
    deleteUserForm.submit();
  });

  deleteProfileCancelButton.addEventListener("click", (event) => {
    event.preventDefault();
    deleteProfileModal.close();
  });
};
