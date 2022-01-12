import {getBackupFiles, downloadBackup} from "./api.js";

export {addDownloadHandlers};

const handleBackupFilters = () => {
    try {
        [
            document.querySelector("#base-name"),
            document.querySelector("#backup-month")
        ].forEach(field => field.addEventListener('change', () => getBackupFiles()));

        getBackupFiles()
    } catch (_) {
    }
}

const addDownloadHandlers = () => {
    const backup_rows = document.querySelectorAll(".backup-table__row")
    backup_rows.forEach(backup_row => {
        backup_row.addEventListener('click', evt => downloadBackup(evt.target.parentNode))
    })
}

handleBackupFilters()
