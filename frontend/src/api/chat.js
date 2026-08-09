export async function sendChat(message, sessionId) {
    const query = new URLSearchParams({ message, session_id: sessionId });
    const response = await fetch(`/api/chat?${query.toString()}`, {
        method: 'GET',
        headers: { Accept: 'application/json' },
    });
    if (!response.ok) {
        throw new Error(`请求失败（${response.status}）`);
    }
    return response.json();
}
