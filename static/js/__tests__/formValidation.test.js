/**
 * @jest-environment jsdom
 */

import { validateInput } from "../formValidation.js";

describe("validateInput function", () => {
  let inputElement;
  let firstNameElement;
  let lastNameElement;

  // Setup a DOM element before each test
  beforeEach(() => {
    // Setup the document body with an input and a span for errors
    document.body.innerHTML = `
      <input type="text" />
      <div>
        <input type="text" name="first_name" maxlength="40" />
      </div>
      <div>
        <input type="text" name="last_name" />
      </div>
    `;
    inputElement = document.querySelector("input");
    firstNameElement = document.querySelector("input[name=first_name]");
    lastNameElement = document.querySelector("input[name=last_name]");
    firstNameElement.dataset.touched = "true";
    lastNameElement.dataset.touched = "true";
    inputElement.dataset.touched = "true";
  });

  test("function exists", () => {
    // Check that the function is defined
    expect(validateInput).toBeDefined();
  });

  test("shows error if input is empty, touched and required", () => {
    inputElement.value = ""; // Set the value of the input to an empty string
    validateInput({ input: inputElement, required: true }); // Call validate function

    validateInput({ input: inputElement }); // Call validate function
    // Check if the error message is shown
    const errorSpan = inputElement.nextElementSibling;
    expect(errorSpan).not.toBeNull();
    expect(errorSpan.classList.contains("hidden")).toBe(false);
  });

  test("shows error if input is multiple spaces", () => {
    inputElement.value = "   "; // Set the value of the input to multiple spaces
    validateInput({ input: inputElement }); // Call validate function
    // Check if the error message is shown
    const errorSpan = inputElement.nextElementSibling;
    expect(errorSpan).not.toBeNull();
    expect(errorSpan.classList.contains("hidden")).toBe(false);
  });

  test("shows error if input is less than 2 characters", () => {
    inputElement.value = "a"; // Set the value of the input to 1 character
    validateInput({ input: inputElement }); // Call validate function
    // Check if the error message is shown
    const errorSpan = inputElement.nextElementSibling;
    expect(errorSpan).not.toBeNull();
    expect(errorSpan.classList.contains("hidden")).toBe(false);
  });
});
