import {getPaginationActionLogs} from "./api.js";

export {renderActionLogs}

const renderActionLogs = async (page, add_more) => {
    const action_logs_list = document.querySelector('.logs__list');

    if (!add_more) {
        action_logs_list.innerHTML = `
            <div class="logs__grid logs__grid_header">
                <span class="logs__id">ID</span>
                <span class="logs__username">Пользователь</span>
                <span class="logs__type">Тип</span>
                <span class="logs__message">Сообщение</span>
                <span class="logs__datetime">Дата</span>
                <span class="logs__ip">IP</span>
            </div>
        `; // Очищаем список
    }

    const logs_response = await getPaginationActionLogs(page, 20);
    logs_response.forEach(log => {
        action_logs_list.innerHTML += `
            <div class="logs__grid">
                <span class="logs__id">#${log['id']}</span>
                <span class="logs__username">${log['user']}</span>
                <span class="logs__type">${log['type']}</span>
                <span class="logs__message">${log['message']}</span>
                <span class="logs__datetime">${new Date(log['date']).toLocaleString("ru-RU", {timeZone: "UTC"})}</span>
                <span class="logs__ip">${log['ip']}</span>
            </div>
        `
    })

    return !(logs_response.some(logs => logs['id'] === 0) || !logs_response.length)
}
