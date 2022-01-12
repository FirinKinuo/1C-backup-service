export {getBasesNames, postAliasName}

const getBasesNames = async () => {
    const requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };
    const bases_names = await fetch(`${window.location.origin}/one-c-base/names`, requestOptions);
    return await bases_names.json()
}


const postAliasName = async (original_name, alias_name) => {
    const headers = new Headers();
    headers.append("Content-Type", "application/json");

    const payload = JSON.stringify({
        "original_name": original_name,
        "alias_name": alias_name,
        "share": true
    });

    const requestOptions = {
        method: 'PUT',
        headers: headers,
        body: payload,
        redirect: 'follow'
    };

    const response = await fetch(`${window.location.origin}/one-c-base/set-alias`, requestOptions)
    return response.status
}