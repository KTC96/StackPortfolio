// @ts-check
import { validateInput } from "./formValidation.js";

const formData = {};

/**
 * Update step counter to show current step
 * and show completed steps
 * @param {number} currentStepIndex
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
    const stepNumber = step?.querySelector(".step-item");
    const stepText = step?.querySelector("span:not(.step-item)");

    if (!stepNumber || !stepText)
      throw new Error("Step number or text not found");

    if (index < currentStepIndex) {
      stepNumber.textContent = "✓";
      stepNumber.classList.add("bg-primary", "text-white");
      stepText.classList.add("text-primary");
    } else if (index === currentStepIndex) {
      stepNumber.textContent = String(index + 1);
      stepNumber.classList.remove("text-white", "bg-secondary");
      stepNumber.classList.add("bg-primary", "text-white");
      stepText.classList.add("text-primary");
    } else {
      stepNumber.textContent = String(index + 1);
      stepNumber.classList.remove("text-primary", "bg-aliceblue");
      stepText.classList.remove("text-primary");
    }
  }
};

/**
 * Update button state
 * @param {Element} button
 * @param {boolean} isValid
 * @returns {void}
 */
const updateButtonState = (button, isValid) => {
  if (button instanceof HTMLButtonElement) {
    button.disabled = !isValid;
  }
  button.classList.toggle("btn-primary", isValid);
  button.classList.toggle("btn-disabled", !isValid);
};

/**
 * Check if step is final step (Summary)
 * for form submission
 * @param {number} index
 * @param {Element[]} steps
 * @returns {boolean}
 */
const isFinalStep = (index, steps) => {
  return index === steps.length - 1;
};

/**
 * Show step
 * @param {Element[]} steps
 * @param {number} currentStepIndex
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
 * Check if step is valid
 * @param {Element[]} steps
 * @param {number} index
 * @returns {boolean}
 */
const isStepValid = (steps, index) => {
  const currentStepInputs = steps[index].querySelectorAll(
    "input:not([type='checkbox']):not([type='radio']):not([type='file']):not([type='hidden']), textarea"
  );

  return [...currentStepInputs].every((input) => {
    if (input instanceof HTMLInputElement) {
      return input.checkValidity();
    } else if (input instanceof HTMLTextAreaElement) {
      return input.checkValidity();
    }
  });
};
/**
 * Setup input listeners
 * @param {Element[]} steps
 * @param {Element[]} nextButtons
 * @returns {void}
 */
const setupInputListeners = (steps, nextButtons) => {
  const textInputs = [
    ...document.querySelectorAll("input:not([type=checkbox]), textarea"),
  ];
  const checkboxInputs = [...document.querySelectorAll("input[type=checkbox]")];

  for (const checkboxInput of checkboxInputs) {
    checkboxInput.addEventListener("change", () => {
      if (checkboxInput instanceof HTMLInputElement) {
        if (checkboxInput.checked) {
          checkboxInput.classList.add("toggle-primary");
          checkboxInput.classList.remove("toggle-secondary");
        } else {
          checkboxInput.classList.remove("toggle-primary");
          checkboxInput.classList.add("toggle-secondary");
        }
      }
    });
  }

  for (const input of textInputs) {
    input.addEventListener("input", () => {
      if (input instanceof HTMLInputElement) {
        input.dataset.touched = "true";

        if (input.name === "first_name" || input.name === "last_name") {
          validateInput({
            input,
            customMaxLength: 40,
            customRequired: true,
          });
        }

        if (input.type === "tel") {
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
        } else if (input.type === "password") {
          const passwordRegex =
            // prettier-ignore
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*#?&_])[A-Za-z\\d@$!%*#?&_]{8,}$";

          validateInput({
            input,
            customPattern: passwordRegex,
            customValidationMessage:
              "Password must be at least 8 characters long, include a number, an uppercase letter, and a special character.",
          });
        } else {
          validateInput({ input });
        }

        if (input.name === "password2") {
          const password1 = document?.getElementById("id_password1");
          // @ts-ignore
          if (password1.value !== input.value) {
            validateInput({
              input,
              customValidationMessage: "Passwords do not match.",
              // @ts-ignore
              customPattern: `${password1.value}{${password1.value.length},}`,
            });
          }
        }
      }

      // @ts-ignore
      if (input.type !== "password") {
        // @ts-ignore
        formData[input.name] = input.value.trim();
        saveFormDataToLocalStorage(formData);
      }

      // After each input event, check the validity of the entire step
      const stepIndex = steps.findIndex((step) => step.contains(input));
      const currentStepIsValid = isStepValid(steps, stepIndex);
      const currentButton = nextButtons[stepIndex];
      updateButtonState(currentButton, currentStepIsValid);
    });
  }
};

/**
 * Setup previous button listeners
 * @param {Element[]} steps
 * @param {Element[]} prevButtons
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
 * Save input to local storage
 * @param {object} formData
 * @returns {void}
 */
const saveFormDataToLocalStorage = (formData) => {
  localStorage.setItem("formData", JSON.stringify(formData));
};

/**
 * Clear local storage
 * @returns {void}
 */
const clearLocalStorage = () => {
  localStorage.clear();
};

/**
 * Display summary details on the summary page
 * @returns {void}
 * */
const displaySummaryDetails = () => {
  // Retrieve the form data from localStorage
  const storedFormData = JSON.parse(localStorage.getItem("formData") || "");

  console.log(storedFormData);

  for (const [key, value] of Object.entries(storedFormData)) {
    const element = document.querySelector(
      // @ts-ignore
      `.${key}-field`.replaceAll("_", "-")
    );
    if (element) {
      element.textContent = value;
    }
  }
};

/**
 * Signup stepper form
 * @returns {void}
 */
const runSignupStepper = () => {
  const nextButtons = [...document.querySelectorAll(".next-button")];
  const prevButtons = [...document.querySelectorAll(".prev-button")];
  const steps = [...document.querySelectorAll("div[data-step]")];

  showStep(steps, 0);

  setupInputListeners(steps, nextButtons);
  setupPreviousButtonListeners(steps, prevButtons);

  for (const [index, step] of steps.entries()) {
    const currentStepIsValid = isStepValid(steps, index);
    const currentButton = nextButtons[index];
    updateButtonState(currentButton, currentStepIsValid);
  }

  for (const [index, button] of nextButtons.entries()) {
    if (button instanceof HTMLButtonElement) {
      button.disabled = true;
    }
    button.classList.add("btn-disabled");
    button.classList.remove("btn-primary");
    button.addEventListener("click", (event) => {
      if (isFinalStep(index, steps)) {
        clearLocalStorage();
      } else {
        // validates inputs before moving to the next step
        if (!isStepValid(steps, index)) return;
        event.preventDefault();
        showStep(steps, index + 1);
        updateStepCounter(index + 1);
      }
      updateButtonState(button, isStepValid(steps, index));
    });

    updateButtonState(button, isStepValid(steps, index));
  }
};

export { runSignupStepper };
