# Heroku Slack agent reference

This skill is for Slack Bolt JavaScript or TypeScript apps on Heroku. If the repo is Python, Java, or another Slack stack, use the platform's native deployment guidance instead of forcing the Bolt JS workflow.

## Recommended runtime split

- Prefer HTTP Request URLs for Slack apps deployed on Heroku that need stable public endpoints, distribution, slash commands, Events API subscriptions, or interactive payload handling over HTTPS.
- Prefer Socket Mode when the app should avoid public inbound request URLs and a worker process is acceptable.
- For Bolt on Heroku, HTTP mode usually means a `web` dyno and Socket Mode usually means a `worker` dyno.

## Procfile patterns

HTTP mode:

```bash
web: node app.js
```

Socket Mode:

```bash
worker: node app.js
```

If the app uses HTTP, make sure it listens on `process.env.PORT`.

## Heroku deployment commands

```bash
heroku git:remote -a <app>
heroku config:set SLACK_SIGNING_SECRET=<secret> SLACK_BOT_TOKEN=xoxb-... -a <app>
git push heroku <branch>:main
heroku ps:scale web=1 -a <app>
```

Socket Mode usually adds `SLACK_APP_TOKEN=xapp-...` and scales a worker instead:

```bash
heroku config:set SLACK_BOT_TOKEN=xoxb-... SLACK_APP_TOKEN=xapp-... -a <app>
heroku ps:scale worker=1 -a <app>
```

## Safe config inspection guidance

- Do not run `heroku config -a <app>` or `heroku config --json -a <app>` in a shared transcript just to inspect Slack settings because those commands reveal current secret values.
- Prefer presence and naming checks from:
  - `.env.example`
  - app manifest files
  - framework initialization code
  - explicit user confirmation from the Heroku dashboard
- If the user explicitly needs one specific config var value checked, use `heroku config:get <VAR_NAME> -a <app>` only for that single variable and redact it in summaries.
- If the user is ready to set or replace secrets, use targeted `heroku config:set` commands instead of broad inspection.

## Slack app manifest and settings fields

For HTTP Request URL apps, the manifest may need:

- `settings.event_subscriptions.request_url`
- `settings.interactivity.request_url`
- `features.slash_commands[].url`

For Socket Mode apps, the manifest may need:

- `settings.socket_mode_enabled`

Common Bolt path:

```text
/slack/events
```

If using Bolt's default receiver, route Events API, interactivity, and slash command URLs to the deployed `/slack/events` endpoint unless the app intentionally uses custom paths.

## Security and correctness notes

- Slack signs inbound HTTP requests. Verify them with the signing secret; Bolt handles this automatically when configured correctly.
- Slash commands and interactive payloads must be acknowledged quickly. Avoid long synchronous work on the request path.
- Keep Slack tokens and secrets in Heroku config vars, not in source control.
- Do not assume Socket Mode is the best production fit on Heroku just because it is convenient in local development.

## Suggested inspection commands

```bash
heroku apps:info -a <app> --json
heroku logs -a <app> --num 200
heroku ps -a <app>
```

## Official docs

- <https://docs.slack.dev/tools/bolt-js/deployments/heroku/>
- <https://docs.slack.dev/tools/bolt-js/building-an-app/>
- <https://docs.slack.dev/reference/app-manifest/>
- <https://docs.slack.dev/authentication/verifying-requests-from-slack/>
- <https://devcenter.heroku.com/articles/preparing-a-codebase-for-heroku-deployment>
