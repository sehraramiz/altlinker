webhook-set:
	curl -F "url=${WEBHOOK_URL}" "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook"

webhook-delete:
	curl "https://api.telegram.org/bot${BOT_TOKEN}/deleteWebhook"

webhook-info:
	curl "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo"

