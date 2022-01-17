import {renderActionLogs} from "./render.js";

export {loadLogs}

let next_page = 2;
let is_loading = true

const loadLogs = async scroll_pos => {
    if (document.body.scrollHeight - window.innerHeight - scroll_pos < 100 && is_loading) {
        is_loading = false;
        if (await renderActionLogs(next_page, true)) {
            next_page++;
            is_loading = true;
        }
    }
};
