const renderBackupFiles = (backup_year_group) => {
  const backup_list = document.querySelector('.backup-list')
  backup_list.innerHTML = ''

  const render_download_backup_file_list = (backup_file_list) => {
    let rendered_backup_button = "";

    backup_file_list.forEach(file => {
      rendered_backup_button += `<a class="backup-list__file" href="${file['file_url']}">
        <span class="backup-list__day">День: ${new Date(file['date']).getDate()}</span>
        <span class="backup-list__size">${(file['size'] / 1024).toFixed(2)} GB</span></a>`
    })

    return rendered_backup_button
  }

  backup_year_group.forEach(backup_file => {
    backup_list.innerHTML += `
        <div class="backup-list_element">
            <h1 class="backup-list__year">${backup_file['year']}</h1>
            <div class="backup-list__table">
                ${render_download_backup_file_list(backup_file['files'])}
            </div>
        </div>
    `
  })
}

const getBackupFiles = () => {
  const base_name = document.querySelector("#base-name");
  const backup_month = document.querySelector("#backup-month");

  const requestOptions = {
    method: 'GET',
    redirect: 'follow'
  };

  fetch(
      `${window.location.origin}/getBackupFiles?base_name=${base_name.value}&month_id=${backup_month.value}`,
      requestOptions)
      .then(response => response.json())
      .then(result => renderBackupFiles(result['year_group']))
      .catch(error => console.log('error', error));
}

[
  document.querySelector("#base-name"),
  document.querySelector("#backup-month")
].forEach(field => field.addEventListener('change', () => getBackupFiles()));
