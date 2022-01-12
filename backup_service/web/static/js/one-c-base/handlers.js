import {
    changeVisibility,
    expandInputField,
    raiseErrorAlert,
    raiseSuccessAlert,
    setAliasesCheckState
} from "./animations.js";
import {postAliasName} from "./api.js";

export {handleInputsAliasName, handleAcceptChangeAlias};

const animateInputsAlias = (target) => {
    expandInputField(target);

    target.labels.forEach(label => {
        changeVisibility(label, label.control.value !== label.control.id, "flex")
    })
}

const handleInputsAliasName = async () => {
    const alias_inputs = document.querySelectorAll(".aliases__change");
    await alias_inputs.forEach(alias => {
        ["keyup", "keydown", "change"].forEach(action => alias.addEventListener(action, async evt => {
            animateInputsAlias(evt.target);
            changeVisibility(
                evt.target.parentElement.querySelector('.aliases_manage'),
                evt.target.value !== evt.target.defaultValue,
                "flex");

            switch (evt.keyCode) {
                case 13: // Клавиша Enter
                    await handleSendingAliasData(evt.target);
                    break;
                case 27: // Клавиша Escape
                    evt.target.value = evt.target.defaultValue;
            }
        }))

        alias.addEventListener("focus", evt => {
            setAliasesCheckState(evt.target.previousElementSibling, 'change')
        })

        alias.addEventListener("blur", evt => {
            setAliasesCheckState(evt.target.previousElementSibling, 'clear')
        })
        animateInputsAlias(alias)
    })
}

const handleSendingAliasData = async (alias_input) => {
    let response_code;
    if (1 <= alias_input.value <= 32 && alias_input.value) {
        response_code = await postAliasName(alias_input.id, alias_input.value)
    } else {
        response_code = await postAliasName(alias_input.id, alias_input.id)

        switch (response_code) {
            case 200:
            case 201:
                alias_input.value = alias_input.id
                break
        }
    }

    switch (response_code) {
        case 200:
            raiseSuccessAlert("Успешно обновлено!")
            alias_input.defaultValue = alias_input.value
            break
        case 201:
            raiseSuccessAlert("Успешно добавлено!")
            alias_input.defaultValue = alias_input.value
            break
        default:
            raiseErrorAlert("Ошибка, повторите запрос")
    }
}

const handleAcceptChangeAlias = async () => {
    const alias_accept_buttons = document.querySelectorAll(".aliases__accept");

    await alias_accept_buttons.forEach(button => button.addEventListener("click", async evt => {
        const input_field = evt.target.closest(".aliases__accept").offsetParent.querySelector('input');
        await handleSendingAliasData(input_field)

        changeVisibility(
            input_field.parentElement.querySelector('.aliases_manage'),
            input_field.value !== input_field.defaultValue,
            "flex")
        animateInputsAlias(input_field)
    }))
}