# Status Bot
This refresh every 120 seconds a message and DM user when service is down !

# Deploy
create
> `bot.ini` file

sample bot.ini
```
[Bot]
Token=bot token
Invite=bot invite link
LogsChannel=log channel id
StatusChannel=status channel id
User=user id will recieve dms
```

and type in a terminal
```shell
python3 main.py --config bot.ini
``` 

Just enjoy !