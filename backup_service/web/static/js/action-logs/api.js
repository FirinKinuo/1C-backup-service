export {getPaginationActionLogs}

const getPaginationActionLogs = async (page, per_page) => {
    const headers = new Headers();
    headers.append("Content-Type", "application/json");

    const requestOptions = {
        method: 'GET',
        headers: headers,
        redirect: 'follow'
    };

    const response = await fetch(
        `${window.location.origin}/logs/getActions?page=${page}&per_page=${per_page}`,
        requestOptions)

    return await response.json()
}
