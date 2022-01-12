import {renderBackupFiles} from "./render.js";

export {getBackupFiles, downloadBackup}

const downloadBackup = (backup_target) => {
    const backup_file = backup_target.getAttribute("data-backup");

    window.open(`${window.location.origin}/download?backup=${backup_file}`, '_blank');
}

const getBackupFiles = () => {
    const base_name = document.querySelector("#base-name");
    const backup_month = document.querySelector("#backup-month");

    if (base_name.value && backup_month.value) {
        const requestOptions = {
            method: 'GET',
            redirect: 'follow'
        };

        fetch(
            `${window.location.origin}/getBackupFiles?base_name=${base_name.value}&month_id=${backup_month.value}`,
            requestOptions)
            .then(response => response.json())
            .then(result => renderBackupFiles(result))
            .catch(() => {
            });
    }
}
