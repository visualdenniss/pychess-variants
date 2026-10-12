export function notify(title: string | null, options: NotificationOptions | undefined) {
    if (!title || !('Notification' in window)) return;

    // Like lila's ui/lib/src/notification.ts, keep delivery outside move processing.
    setTimeout(() => {
        const show = () => {
            const notification = new Notification(title, options);
            notification.onclick = () => window.focus();
        };

        try {
            if (Notification.permission === 'granted') {
                show();
            } else if (Notification.permission === 'default') {
                void Notification.requestPermission()
                    .then(permission => {
                        if (permission === 'granted') show();
                    })
                    .catch(() => {});
            }
        } catch {
            // Some browsers expose the API but reject permission requests or construction.
        }
    }, 0);
}
