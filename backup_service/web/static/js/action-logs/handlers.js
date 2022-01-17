import {loadLogs} from "./scroll-loading.js";

export {addScrollHandler}

const addScrollHandler = async () => {
    window.addEventListener('scroll', () => {
        window.requestAnimationFrame(async () => {
            await loadLogs(window.scrollY);
        });
    });
};
