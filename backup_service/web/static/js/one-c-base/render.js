import {handleInputsAliasName, handleAcceptChangeAlias} from "./handlers.js";
import {getBasesNames} from "./api.js";

export {renderAliasNamesChange, renderAlert}

const renderAliasNamesChange = async () => {
    const alias_names_grid = document.querySelector(".aliases__grid");
    alias_names_grid.innerHTML = ''; // Очищаем таблицу

    let bases_names = await getBasesNames();
    bases_names = bases_names.sort((self, other) => self['alias_name'] < other['alias_name'] ? -1 : 1);

    bases_names.forEach(base => {
        alias_names_grid.innerHTML += `
        <div class="aliases__field">
            <div class="aliases__checkbox"></div>
            <input type="text" class="aliases__change" minlength="1" maxlength="32" id=${base['original_name']} value='${base['alias_name']}'>
            
            <menu class="aliases_manage">
                <menuitem class="aliases__accept" data-change-alias=${base['original_name']}>
                    <span class="iconify" data-icon="bx:bx-save"></span>
                </menuitem>
            </menu>
            
            <label class="aliases__original" for=${base['original_name']}>
                ${base['original_name']}
            </label>
        </div>
        `
    });

    handleInputsAliasName();
    await handleAcceptChangeAlias();
}

const renderAlert = (message, type) => {
    const type_accent = {
        'success': "#55DE8C",
        'error': "#DE5586"
    }

    const alert = document.createElement('span');
    alert.className = "aliases__alert";

    alert.innerText = message;

    const alert_wrap = document.createElement('div');
    alert_wrap.className = "aliases__alert-wrap";
    alert_wrap.style.background = `linear-gradient(252.74deg, ${type_accent[type]} -12.01%, #78BFD6 94.9%)`

    alert_wrap.appendChild(alert)

    const body = document.body

    body.insertBefore(alert_wrap, document.querySelector(".aliases__wrap"))

    return alert_wrap
}

