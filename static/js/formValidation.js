//@ts-check

/**
 * @typedef {Object} ValidationResult
 * @property {boolean} isValid - Indicates if the input is valid
 * @property {string} errorMessage - The error message, if any
 */

/**
 * ValidateTextInput validates a text input, using standard
 * HTML5 validation, then calls the function to create an
 * error message. Parameters can be added to override the
 * validation requirements and error message.
 *
 * @param {Object} inputDetailsObj - An object containing the input details
 * @param {HTMLInputElement} inputDetailsObj.input - The input element to validate
 * @param {boolean} [inputDetailsObj.customRequired] - Whether the input is required
 * @param {string} [inputDetailsObj.customValidationMessage=''] - The error message to display
 * @param {number} [inputDetailsObj.customMinLength=0] - The minimum length of the input
 * @param {number} [inputDetailsObj.customMaxLength=Infinity] - The maximum length of the input
 * @param {string} [inputDetailsObj.customPattern=''] - A regex pattern to validate the input against
 * @returns {void}
 *
 * @example validateInput({ input, required: true, validationMessage: "Please enter a valid first name.", minLength: 0, maxLength: 40, pattern: "^[a-zA-Z]+$" })
 * @example validateInput({ input, required: true, validationMessage: "Please enter a valid last name.", minLength: 0 })
 * @example validateInput({ input, required: true, validationMessage: "Please enter a valid name." })
 */
const validateInput = (inputDetailsObj) => {
  const {
    input,
    customRequired = false,
    customValidationMessage = "",
    customMinLength = 0,
    customMaxLength = Infinity,
    customPattern = "",
  } = inputDetailsObj;

  const isRequired = customRequired || input.required;
  const validationMessage =
    customValidationMessage || input.validationMessage || "";
  const minLength = customMinLength || input.minLength || 0;
  const maxLength = customMaxLength || input.maxLength || Infinity;
  const pattern = customPattern || input.pattern || "";

  if (customMaxLength) input.maxLength = customMaxLength;
  let isValid = input.checkValidity();
  let errorMessage = "";

  if (input.validity.valueMissing) {
    errorMessage = isRequired ? validationMessage : "";
    isValid = false;
  }

  if (input.validity.tooShort) {
    errorMessage = `Please lengthen this text to ${minLength} characters or more`;
    isValid = false;
  }

  if (input.validity.tooLong) {
    errorMessage = `Please shorten this text to ${maxLength} characters or fewer`;
    isValid = false;
  }

  if (input.value && !RegExp(pattern).test(input.value)) {
    errorMessage = customValidationMessage || input.validationMessage;
    isValid = false;
  }

  input.setCustomValidity(errorMessage);
  isValid = input.checkValidity();

  return isValid ? removeErrorSpan(input) : generateErrorSpan(input);
};

/**
 * Generate error span element
 * @param {HTMLInputElement} input - The input element to add the error message
 * @returns {void}
 */
const generateErrorSpan = (input) => {
  input.classList.remove("input-valid");
  input.classList.add("input-invalid");
  const errorSpan =
    input.nextElementSibling?.classList.contains("error-span") &&
    input.nextElementSibling instanceof HTMLSpanElement
      ? input.nextElementSibling
      : document.createElement("span");

  errorSpan.textContent = input.validationMessage;
  errorSpan.setAttribute("role", "alert");
  errorSpan.setAttribute("aria-live", "assertive");
  errorSpan.classList.add("error-span", "text-error", "text-sm", "mt-2");
  input.insertAdjacentElement("afterend", errorSpan);
};

/**
 * Remove error span element
 * @param {HTMLInputElement} input - The input element to remove the error message
 * @returns {void}
 */
const removeErrorSpan = (input) => {
  input.classList.remove("input-invalid");
  input.classList.add("input-valid");
  const errorSpan = input.nextElementSibling;
  if (errorSpan && errorSpan.classList.contains("error-span")) {
    errorSpan.remove();
  }
};

export { validateInput, generateErrorSpan, removeErrorSpan };
