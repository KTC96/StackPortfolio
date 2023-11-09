/**
 * @jest-environment jsdom
 */

import { validateInput } from "../formValidation.js";

describe("validateInput function", () => {
  let inputElement;
  let firstNameElement;
  let lastNameElement;
  let firstNameErrorSpan;
  let lastNameErrorSpan;
  let errorSpan;

  // Setup a DOM element before each test
  beforeEach(() => {
    // Setup the document body with an input and a span for errors
    document.body.innerHTML = `
      <input type="text" />
      <span class="error-span hidden"></span>
      <div>
        <input type="text" name="first_name" />
        <span class="first-name-error-span error-span hidden"></span>
      </div>
      <div>
        <input type="text" name="last_name" />
        <span class="last-name-error-span error-span hidden"></span>
      </div>
    `;
    inputElement = document.querySelector("input");
    firstNameElement = document.querySelector("input[name=first_name]");
    lastNameElement = document.querySelector("input[name=last_name]");
    firstNameElement.dataset.touched = "true";
    lastNameElement.dataset.touched = "true";
    inputElement.dataset.touched = "true";
    firstNameErrorSpan = document.querySelector(".first-name-error-span");
    lastNameErrorSpan = document.querySelector(".last-name-error-span");
    errorSpan = document.querySelector(".error-span");
  });

  test("function exists", () => {
    // Check that the function is defined
    expect(validateInput).toBeDefined();
  });

  test("returns false if input is empty", () => {
    inputElement.value = ""; // Set the value of the input to an empty string
    expect(validateInput(inputElement)).toBeFalsy();
    // Check if the error message is shown
    expect(errorSpan.classList.contains("hidden")).toBe(false);
  });

  test("returns false if input multiple spaces", () => {
    inputElement.value = "   "; // Set the value of the input to multiple spaces
    const isValid = validateInput(inputElement);
    expect(isValid).toBeFalsy();
    // Check if the error message is shown
    expect(errorSpan.classList.contains("hidden")).toBe(false);
  });

  test("returns false if input is less than 2 characters", () => {
    inputElement.value = "a"; // Set the value of the input to 1 character
    const isValid = validateInput(inputElement);
    expect(isValid).toBeFalsy();
    // Check if the error message is shown
    expect(errorSpan.classList.contains("hidden")).toBe(false);
  });

  test("returns false if first_name or last_name is more than 41 characters", () => {
    firstNameElement.value = "a".repeat(42); // Set the value of the input to 42 characters
    lastNameElement.value = "a".repeat(42); // Set the value of the input to 42 characters
    const isValid = validateInput(firstNameElement);
    expect(isValid).toBeFalsy();
    // Check if the error message is shown
    expect(firstNameErrorSpan.classList.contains("hidden")).toBe(false);
  });
});
