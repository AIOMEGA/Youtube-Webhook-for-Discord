# YouTube → Discord Notifier

This project was requested by a friend.

It uses **GitHub Gist**, **GitHub Secrets**, **GitHub Variables**, and the **YouTube Data API v3**.  
Since most YouTube bots and webhook tools are either deprecated or require payment, this simple Python script provides a free and working alternative.

---

## ✅ Features

- Automatically checks a YouTube channel every 5 minutes
- Compares the ID of the most recent video to a saved ID in a Gist
- Updates the saved ID if a new video is detected
- Sends a custom Discord webhook notification to a set channel and role

> ⚠️ **Note:** This webhook is customized for my friend's Discord server, so it won’t work for others without modification.

---

## 🚀 Setup Guide
If you would like to make this work for you, follow these steps.
1. Fork and Clone the repository.
2. In youtube_notifier.py replace the values for `CHANNEL_ID`, `UPLOADS_PLAYLIST_ID` with equivalent IDs for your channel.
3. On your repository go Settings -> Secrets and variables -> Actions and create your own GitHub secrets for WEBHOOK_URL, GIST_ID, GITHUB_TOKEN and YOUTUBE_API_KEY if they don't already exist. **The following steps will tell you how to get the value for each secret**.
4. On your Discord server add a Webhook, set the channel you want it to post in and copy the Webhook URL, paste it as the value for WEBHOOK_URL.
5. Go to https://gist.github.com/ and set the file name as "last_video_id.txt" and set the description as "test123" then create it.
6. In the URL of the gist you created you should see something like https://gist.github.com/You/112abc456, copy the 123abc456 and put that as the value of GIST_ID.
7. Next go to https://github.com/settings/tokens and create a classic token, give it the description "gist-read-write" (experation date up to you, personally I set to never expire). Then select the checkbox for gist **ONLY** and generate the token.
8. Copy the token ID and set it as the value for GITHUB_TOKEN.
9. Finally you will need to go to https://console.cloud.google.com/apis/credentials create a project, then search for "youtube data api v3" select the Google api and go to the credentials tab, click "+ create credentials" and select API key.
10. Copy the key and put it as the value for YOUTUBE_API_KEY.
11. Now add, commit and push the changes to your Repository.
12. Finally go to the Actions tab on your repository and select the "YouTube Check and Discord Notify" action, select to run the workflow on the main branch and the Webhook should start automatically checking your channel for new uploads and notifying your server. 
