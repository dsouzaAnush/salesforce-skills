# AppLink publications reference

## Inspect current state

```bash
heroku salesforce:publications -a <app> [--addon <addon>] [--connection_name <connection>]
```

## Publish

```bash
heroku salesforce:publish <API_SPEC_FILE_DIR> -a <app> -c <client-name> --connection-name <connection> [--addon <addon>] [--metadata-dir <dir>]
```

## Operational guidance

- AppLink creates external services, API Catalog entries, and Agentforce agent actions when you publish.
- Review which shared publication endpoints or shared objects will be visible before you publish.
- Review the OpenAPI 3.0 spec carefully before publishing.
- Only connected orgs can invoke published apps.
- The AppLink service mesh validates inbound calls and provides scoped tokens.
- Choose the right user mode: `user`, `user-plus`, or `authorized-user`.

## Current considerations

- As of Salesforce Spring '26, avoid relying on `--authorization-connected-app-name` and `--authorization-permission-set-name` for new connected apps unless your org has the required Salesforce permission enabled.
- Keep production and sandbox publications aligned with matching environment types.

## Official docs

- <https://devcenter.heroku.com/articles/heroku-applink>
- <https://devcenter.heroku.com/articles/working-with-heroku-applink>
- <https://devcenter.heroku.com/articles/heroku-applink-cli>
- <https://devcenter.heroku.com/articles/getting-started-heroku-applink-agentforce>
