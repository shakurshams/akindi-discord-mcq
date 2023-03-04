1. Put ```.env``` file in the top level folder /akindi-discord-mcq. Sent the file in email.
2. Run ```docker-compose up```
3. You should see the server running
4. First make sure the channel you want to add the bot to does not have 15 webhooks already. Otherwise it will not allow to add a new one.
5.Now in the browser go to this link:https://discord.com/oauth2/authorize?client_id=1080936200153608202&redirect_uri=https%3A%2F%2Fakindi-discord-mcq.ngrok.io%2Foauth-redirect&response_type=code&scope=webhook.incoming
6. It will ask you to choose your server and the channel you want to add the bot to. Make sure you are permitted to add the bot.
7. After clicking the Authorize button, you should see a success response message.
8. Now to post a questin to this channel, make this curl request:
```curl --location --request GET '0.0.0.0:5000/send_question/<question_id>'```
example:
```curl --location --request GET '0.0.0.0:5000/send_question/1'```
9. If successful you should see the question with options in the channel which you can interact with.
10. Answer the question and it should tell you if the answer was right or wrong