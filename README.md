# Status Bot
This refresh every 120 seconds a message and DM user when service is down !

# Deploy
rename
> `bot.sample.ini` in`bot.ini` file

and add your personal information:
```
[Bot]
Token=bot token
Invite=bot invite link
LogsChannel=log channel id
StatusChannel=status channel id
User=user id will recieve dms
```
rename
> `to_check.sample.json` in`to_check.json` file

and add you own data:
```json
{"data":  [
  {"url": "http://example.com", "nom": "Example website", "desc": "example website desc", "notify": true},
  {"url": "https://www.camarm.dev", "nom": "CAMARM Website", "desc": "Site officiel de CAMARM-DEV.", "notify": false}
]}
```

**To check ip/hostname with tcp write `host://ip` / `host://hostname`**

NOTES: `url`: _url of service_ (**string**), `nom`: _the name that will be showed_ (**string**), `desc`: _a description_ (**string**), `notify`: _if on true, a dm will be sent when service is down and embed will be red with an error gif, if on false nothing will happen except the red circle on embed_ (**bool**)

and type in a terminal
```shell
python3 main.py --config bot.ini
``` 

Just enjoy !