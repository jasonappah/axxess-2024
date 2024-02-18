const host = "http://localhost:8080";

export function post(url, data) {
    return fetch(host + "/" + url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
}

export function get(url) {
    return fetch(host + "/" + url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
}