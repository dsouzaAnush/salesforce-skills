# AppLink connections reference

## Install and provision

```bash
heroku addons:create heroku-applink -a <app>
heroku plugins:install @heroku-cli/plugin-applink
```

## Salesforce connections

```bash
heroku salesforce:connect <CONNECTION_NAME> -a <app> [--addon <addon>] [--browser <browser>]
heroku salesforce:connect:jwt <CONNECTION_NAME> -a <app> --client-id <client-id> --jwt-key-file <key.pem> --username <user> [--addon <addon>] [--login-url <url>]
```

## Authorizations

```bash
heroku salesforce:authorizations:add <AUTH_NAME> -a <app> [--addon <addon>]
heroku salesforce:authorizations:jwt:add <AUTH_NAME> -a <app> --client-id <client-id> --jwt-key-file <key.pem> --username <user> [--addon <addon>]
heroku datacloud:authorizations:jwt:add <AUTH_NAME> -a <app> --client-id <client-id> --jwt-key-file <key.pem> --username <user> [--addon <addon>]
```

## Working rules

- Connections establish trusted org relationships that publication and invocation flows reuse later.
- Authorizations are for app-initiated access as a specific user.
- Use this workflow for connection setup, connection prerequisites, and connection state checks before any publication work.
- Publications are a separate concern; use an existing connection first, then publish through the publications workflow.
- Do not mix sandbox and production orgs casually; stage them intentionally.
- AppLink requires Salesforce editions with API access.

## Official docs

- <https://devcenter.heroku.com/articles/heroku-applink>
- <https://devcenter.heroku.com/articles/working-with-heroku-applink>
- <https://devcenter.heroku.com/articles/heroku-applink-cli>
- <https://devcenter.heroku.com/articles/heroku-applink-api>
