import {addDownloadHandlers} from "./handlers.js";

export {renderBackupFiles}

const renderBackupFiles = (backup_file) => {
    const backup_table = document.querySelector('.backup-table__body')
    backup_table.innerHTML = '' // Очищаем таблицу

    const renderBackupTable = (backup_data) => {
        let rendered_backup_rows = "";
        const date_params = {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
        };

        backup_data['files'].forEach(file => {
            rendered_backup_rows += `
                <tr class="backup-table__row" data-backup=${file['file_url']}>
                    <td class="backup-table__base">${backup_data['base_name_alias']}</td>
                    <td class="backup-table__date">${new Date(file['date']).toLocaleString('ru', date_params)}</td>
                    <td class="backup-table__size">${(file['size'] / 1024).toFixed(2)} GB</td>
                </tr>`
        });
        return rendered_backup_rows;
    }
    backup_table.innerHTML += renderBackupTable(backup_file)

    addDownloadHandlers();
}
