/**
 * Checks if password1 and 2 fields match
 * @constant passwordCriteria - object containing regex for password criteria
 */
const passwordCriteria = {
  length: new RegExp(".{8,}"), // at least 8 characters
  number: new RegExp("\\d"), // contains a number
  upper: new RegExp("[A-Z]"), // contains an uppercase letter
  special: new RegExp("[^A-Za-z0-9]"), // contains a special character
};

/**
 * Checks if password1 and 2 fields match
 * @param {string} password
 * @returns {boolean}
 * @example validatePasswordCriteria("password1") // returns false
 * @example validatePasswordCriteria("Password1!") // returns true
 */
const validatePasswordCriteria = (password) => {
  return Object.values(passwordCriteria).every((regex) => regex.test(password));
};

const validatePasswordsMatch = () => {
  const password1Input = document.querySelector('input[name="password1"]');
  const password2Input = document.querySelector('input[name="password2"]');
  const passwordErrorSpan = document.querySelector(".password-mismatch-error");
  const passwordCriteriaErrorSpan = document.querySelector(
    ".password-criteria-error"
  );

  let valid = true;

  if (password1Input.dataset.touched && password2Input.dataset.touched) {
    if (password1Input.value !== password2Input.value) {
      passwordErrorSpan.classList.remove("hidden");
      passwordErrorSpan.textContent = "Passwords do not match.";
      password1Input.classList.add("input-invalid");
      password2Input.classList.add("input-invalid");
      valid = false;
    } else {
      passwordErrorSpan.classList.add("hidden");
      password1Input.classList.remove("input-invalid");
      password2Input.classList.remove("input-invalid");
    }
  }

  if (
    !validatePasswordCriteria(password1Input.value) ||
    !validatePasswordCriteria(password2Input.value)
  ) {
    if (passwordCriteriaErrorSpan.classList.contains("hidden")) {
      passwordCriteriaErrorSpan.classList.remove("hidden");
    }
    passwordCriteriaErrorSpan.textContent =
      "Password must be at least 8 characters long, include a number, an uppercase letter, and a special character.";
    password1Input.classList.add("input-invalid");
    password2Input.classList.add("input-invalid");
    valid = false;
  } else {
    passwordCriteriaErrorSpan.classList.add("hidden");
    password1Input.classList.remove("input-invalid");
    password2Input.classList.remove("input-invalid");
  }

  return valid;
};

/**
 * Validate input
 * @param {HTMLInputElement} input
 * @returns {boolean}
 */
const validateInput = (input) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  const phoneNumberRegex = /^\d+$/;
  const errorSpan = input.nextElementSibling;

  // check if input is textarea
  if (input.tagName === "TEXTAREA") {
    if (input.value.length > 0 && input.value.length < 10) {
      input.classList.add("input-invalid");
      errorSpan.classList.remove("hidden");
      errorSpan.textContent = "Bio must be at least 10 characters long.";
      return false;
    } else {
      input.classList.remove("input-invalid");
      errorSpan.classList.add("hidden");
      return true;
    }
  }

  if (!input.dataset.touched) {
    input.classList.remove("input-invalid");
    errorSpan?.classList.add("hidden");
    return !input.required;
  }

  // check if input is multiple spaces
  if (input.value.trim().length < 2) {
    input.classList.remove("input-valid");
    input.classList.add("input-invalid");
    if (input.getAttribute("minlength")) {
      errorSpan.textContent = `This field must contain at least ${input.getAttribute(
        "minlength"
      )} characters.`;
    }

    errorSpan.classList.remove("hidden");
    return false;
  }

  if (input.type === "text" && input.value.trim().length > 40) {
    input.classList.remove("input-valid");
    input.classList.add("input-invalid");
    if (input.getAttribute("maxlength")) {
      errorSpan.textContent = `This field must contain fewer than ${input.getAttribute(
        "maxlength"
      )} characters.`;
    }

    errorSpan.classList.remove("hidden");
    return false;
  }

  let isValid = input.validity.valid;

  if (
    input.name === "phone_number" &&
    input.value &&
    !phoneNumberRegex.test(input.value)
  ) {
    isValid = false;
  }
  if (input.type === "email" && !emailRegex.test(input.value)) {
    isValid = false;
  }

  // If it's one of the password fields, check if passwords match.
  if (input.name === "password1" || input.name === "password2") {
    if (!validatePasswordsMatch()) {
      isValid = false;
      const passwordErrorSpan = document.querySelector(
        ".password-mismatch-error"
      );
      passwordErrorSpan.textContent = "Passwords do not match.";
      if (passwordErrorSpan) {
        passwordErrorSpan.classList.remove("hidden");
      }
    } else {
      const passwordErrorSpan = document.querySelector(
        ".password-mismatch-error"
      );
      if (passwordErrorSpan) {
        passwordErrorSpan.classList.add("hidden");
      }
    }
  }

  if (isValid) {
    input.classList.remove("input-invalid");
    input.classList.add("input-valid");
    errorSpan?.classList.add("hidden");
    return true;
  } else {
    input.classList.add("input-invalid");
    input.classList.remove("input-valid");
    errorSpan?.classList.remove("hidden");
    if (
      input.name === "phone_number" &&
      input.value &&
      !phoneNumberRegex.test(input.value)
    ) {
      errorSpan.innerText = "Phone number must only contain numbers.";
    } else if (input.type === "email" && !emailRegex.test(input.value)) {
      errorSpan.innerText = "Please enter a valid email address.";
    } else {
      errorSpan.textContent = input.validationMessage;
    }

    return false;
  }
};

/**
 * Update button state
 * @param {HTMLButtonElement} button
 * @param {boolean} isValid
 * @returns {void}
 */
const updateButtonState = (button, isValid) => {
  button.disabled = !isValid;
  button.classList.toggle("btn-primary", isValid);
  button.classList.toggle("btn-disabled", !isValid);
  button.classList.toggle("cursor-not-allowed", !isValid);
};

/**
 * Update step counter to show current step
 * and show completed steps
 * @param {number} currentStep
 * @returns {void}
 * */
const updateStepCounter = (currentStepIndex) => {
  // Update mobile steps
  const mobileSteps = document.querySelectorAll(".steps-mobile .step");
  for (const [index, step] of mobileSteps.entries()) {
    if (index < currentStepIndex) {
      step.classList.add("step-primary");
      step.setAttribute("data-content", "✓");
    } else if (index === currentStepIndex) {
      step.classList.add("step-primary");
      step.removeAttribute("data-content");
    } else {
      step.classList.remove("step-primary");
      step.removeAttribute("data-content");
    }
  }

  const desktopSteps = document.querySelectorAll(".steps-desktop .join-item");
  for (const [index, step] of desktopSteps.entries()) {
    const stepNumber = step.querySelector(".step-item");
    const stepText = step.querySelector("span:not(.step-item)");

    if (index < currentStepIndex) {
      stepNumber.textContent = "✓";
      stepNumber.classList.add("bg-primary", "text-white");
      stepText.classList.add("text-primary");
    } else if (index === currentStepIndex) {
      stepNumber.textContent = index + 1; // Keep the number for the current step
      stepNumber.classList.remove("text-white", "bg-secondary");
      stepNumber.classList.add("bg-primary", "text-white");
      stepText.classList.add("text-primary");
    } else {
      stepNumber.textContent = index + 1;
      stepNumber.classList.remove("text-primary", "bg-aliceblue");
      stepText.classList.remove("text-primary");
    }
  }
};

/**
 * Show step
 * @param {HTMLDivElement[]} steps
 * @param {number} currentStep
 * @returns {void}
 */
const showStep = (steps, currentStepIndex) => {
  for (const [index, step] of steps.entries()) {
    step.classList.remove("current-step");
    step.classList.add("hidden");

    if (index === currentStepIndex) {
      step.classList.add("current-step");
      step.classList.remove("hidden");

      if (isFinalStep(index, steps)) {
        displaySummaryDetails();
      }

      // Focusable elements for the current step
      // because users were able to tab outside of the
      // current step
      const focusableElements = [
        ...step.querySelectorAll("input, textarea, select, button"),
      ];
      for (const element of focusableElements) {
        element.removeAttribute("tabindex");
      }
    } else {
      // Unfocusable elements for non-current steps
      const focusableElements = [
        ...step.querySelectorAll("input, textarea, select, button"),
      ];
      for (const element of focusableElements) {
        element.setAttribute("tabindex", "-1");
      }
    }
  }
  updateStepCounter(currentStepIndex);
};

/**
 * Check if step is final step (Summary)
 * for form submission
 * @param {number} index
 * @param {HTMLDivElement[]} steps
 * @returns {boolean}
 */
const isFinalStep = (index, steps) => {
  return index === steps.length - 1;
};

/**
 * Check if step is valid
 * @param {HTMLDivElement[]} steps
 * @param {number} index
 * @returns {boolean}
 */
const isStepValid = (steps, index) => {
  const currentStepInputs = steps[index].querySelectorAll(
    "input:not([type='checkbox']):not([type='radio']), textarea"
  );
  return [...currentStepInputs].every((input) => validateInput(input));
};

/**
 * Save input to local storage
 * @param {HTMLInputElement} input
 * @returns {void}
 */
const saveFormDataToLocalStorage = (formData) => {
  localStorage.setItem("formData", JSON.stringify(formData));
};

/**
 * Skeleton for formData object
 * @constant formData - localStorage obj to store form data
 */
const formData = {
  first_name: "",
  last_name: "",
  email: "",
  username: "",
  town_city: "",
  phone_number: "",
  bio: "",
  work_title: "",
  company: "",
  github_username: "",
  linkedin_username: "",
  twitter_handle: "",
};

/**
 * Display summary details on the summary page
 * @returns {void}
 * */
const displaySummaryDetails = () => {
  // Retrieve the form data from localStorage
  const storedFormData = JSON.parse(localStorage.getItem("formData")) || {};

  // This may be revisited in the future to make it less
  // repetitive
  document.querySelector(".first-name-field").textContent =
    storedFormData.first_name || "";
  document.querySelector(".last-name-field").textContent =
    storedFormData.last_name || "";
  document.querySelector(".email-field").textContent =
    storedFormData.email || "";
  document.querySelector(".username-field").textContent =
    storedFormData.username || "";
  document.querySelector(".town-city-field").textContent =
    storedFormData.town_city || "";
  document.querySelector(".phone-number-field").textContent =
    storedFormData.phone_number || "";
  document.querySelector(".bio-field").textContent = storedFormData.bio || "";
  document.querySelector(".work-title-field").textContent =
    storedFormData.work_title || "";
  document.querySelector(".company-field").textContent =
    storedFormData.company || "";
  document.querySelector(".github-username-field").textContent =
    storedFormData.github_username || "";
  document.querySelector(".linkedin-username-field").textContent =
    storedFormData.linkedin_username || "";
  document.querySelector(".twitter-handle-field").textContent =
    storedFormData.twitter_handle || "";
};

/**
 * Setup input listeners
 * @param {HTMLDivElement[]} steps
 * @param {HTMLButtonElement[]} nextButtons
 * @returns {void}
 */
const setupInputListeners = (steps, nextButtons) => {
  const textInputs = [
    ...document.querySelectorAll("input:not([type=checkbox]), textarea"),
  ];
  const checkboxInputs = [...document.querySelectorAll("input[type=checkbox]")];

  for (const checkboxInput of checkboxInputs) {
    checkboxInput.addEventListener("change", () => {
      checkboxInput.setAttribute("checked", checkboxInput.checked);
    });
  }

  for (const input of textInputs) {
    input.addEventListener("input", () => {
      if (!input.classList.contains("password-field")) {
        input.dataset.touched = "true";
        validateInput(input);
        if (input.type !== "password") {
          formData[input.name] = input.value;
          saveFormDataToLocalStorage(formData);
        }
      }

      // After each input event, check the validity of the entire step
      const stepIndex = steps.findIndex((step) => step.contains(input));
      const currentStepIsValid = isStepValid(steps, stepIndex);
      const currentButton = nextButtons[stepIndex];
      updateButtonState(currentButton, currentStepIsValid);
    });
  }

  // Attach blur event listeners specifically for password fields
  const password1Input = document.querySelector('input[name="password1"]');
  const password2Input = document.querySelector('input[name="password2"]');
  password1Input.addEventListener("blur", validatePasswordsMatch);
  password2Input.addEventListener("blur", validatePasswordsMatch);
};

/**
 * Clear local storage
 * @returns {void}
 */
const clearLocalStorage = () => {
  localStorage.clear();
};

/**
 * Setup previous button listeners
 * @param {HTMLDivElement[]} steps
 * @param {HTMLButtonElement[]} prevButtons
 * @returns {void}
 */
const setupPreviousButtonListeners = (steps, prevButtons) => {
  for (const [index, button] of prevButtons.entries()) {
    button.addEventListener("click", (event) => {
      // Prevents form submission as the
      // button is a submit button by default
      // when it's inside a form
      event.preventDefault();

      // Determine the current step index
      const currentStepIndex = steps.findIndex((step) =>
        step.classList.contains("current-step")
      );
      const previousStepIndex = currentStepIndex - 1;

      // Move to the previous step if it exists
      if (previousStepIndex >= 0) {
        showStep(steps, previousStepIndex);
      }
    });
  }
};

/**
 * Signup stepper form
 * @returns {void}
 */
const runSignupStepper = () => {
  const nextButtons = [...document.querySelectorAll(".next-button")];
  const prevButtons = [...document.querySelectorAll(".prev-button")];
  const steps = [...document.querySelectorAll("[data-step]")];

  showStep(steps, 0);

  setupInputListeners(steps, nextButtons);
  setupPreviousButtonListeners(steps, prevButtons);
  for (const button of nextButtons) {
    button.disabled = true;
    button.classList.add("btn-disabled");
    button.classList.remove("btn-primary");
  }

  for (const [index, step] of steps.entries()) {
    const currentStepIsValid = isStepValid(steps, index);
    const currentButton = nextButtons[index];
    updateButtonState(currentButton, currentStepIsValid);
  }

  for (const [index, button] of nextButtons.entries()) {
    button.addEventListener("click", (event) => {
      if (isFinalStep(index, steps)) {
        clearLocalStorage();
      } else {
        event.preventDefault();
        showStep(steps, index + 1);
        updateStepCounter(index + 1);
      }
      updateButtonState(button, isStepValid(steps, index));
    });

    updateButtonState(button, isStepValid(steps, index));
  }
};

const profileEditValidation = () => {
  // click class edit-profile-step to show id edit_form_profile form
  // click class edit-details-step to show id edit_form_details

  const editProfileStep = document.querySelector(".edit-profile-step");
  const editDetailsStep = document.querySelector(".edit-details-step");

  const editProfileForm = document.querySelector("#edit_form_profile");
  const editDetailsForm = document.querySelector("#edit_form_details");

  editProfileStep.addEventListener("click", (event) => {
    editProfileForm.classList.remove("hidden");
    editDetailsForm.classList.add("hidden");
  });

  editDetailsStep.addEventListener("click", (event) => {
    editProfileForm.classList.add("hidden");
    editDetailsForm.classList.remove("hidden");
  });
};

export { validateInput, runSignupStepper, profileEditValidation };
