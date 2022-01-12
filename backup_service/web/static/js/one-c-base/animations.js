import {renderAlert,} from "./render.js";

export {
    expandInputField,
    changeVisibility,
    raiseSuccessAlert,
    raiseErrorAlert,
    setAliasesCheckState
}

const expandInputField = (input_field) => {
    input_field.style.width = (input_field.value.length || -0.9) + 1 + "ch";
}

const changeVisibility = (element, state, display_type = "inline") => {
    element.style.display = state ? display_type : "none"
}

const raiseAlert = (message, type) => {
    const alert = renderAlert(message, type);

    for (let opacity = 0; opacity <= 1; opacity += 0.1) {
        setTimeout(() => alert.style.opacity = `${opacity}`, 100);
    }

    setTimeout(() => alert.remove(), 2500);
}

const raiseSuccessAlert = (message) => raiseAlert(message, "success");
const raiseErrorAlert = (message) => raiseAlert(message, "error");

const setAliasesCheckState = (checkbox, state) => {
    switch (state) {
        case "change":
            checkbox.style.background = "var(--primary)";
            checkbox.style.borderRadius = "0";
            break;
        case "clear":
            checkbox.removeAttribute("style")
    }
}