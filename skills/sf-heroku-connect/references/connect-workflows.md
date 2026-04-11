# Heroku Connect workflows

## Provision and install

```bash
heroku addons:create heroku-postgresql:<plan> -a <app>
heroku addons:create herokuconnect:<plan> -a <app>
heroku plugins:install @heroku-cli/heroku-connect-plugin
```

## Initial connection setup

```bash
heroku connect:db:set DATABASE_URL -a <app> [--resource <resource>]
heroku connect:sf:auth -a <app> [--resource <resource>]
```

Use these before normal inspection commands on a brand-new setup.

## Inspect and diagnose

```bash
heroku connect:info -a <app> [--resource <resource>]
heroku connect:diagnose -a <app> [--resource <resource>] --verbose
heroku connect:mapping:diagnose <MAPPING> -a <app> [--resource <resource>] --verbose
```

## Mapping management

```bash
heroku connect:export -a <app> [--resource <resource>]
heroku connect:import <FILE> -a <app> [--resource <resource>]
heroku connect:mapping:reload <MAPPING> -a <app> [--resource <resource>]
heroku connect:mapping:write-errors <MAPPING> -a <app> [--resource <resource>] --json
```

## Operational guidance

- The Connect CLI plugin is experimental and not officially supported.
- The Connect API is rate-limited per connection per day.
- Prefer dashboard-based mapping creation for brand-new setups; CLI import is best for repeatable config.
- Distinguish read-only diagnosis from state-changing operations such as `pause`, `resume`, `recover`, `import`, and mapping deletion.
- Remember that a new Heroku Connect setup also needs database selection and Salesforce authorization before sync can work.

## Official docs

- <https://devcenter.heroku.com/articles/heroku-connect>
- <https://devcenter.heroku.com/articles/heroku-connect-api>
- <https://devcenter.heroku.com/articles/heroku-connect-cli>
- <https://devcenter.heroku.com/articles/quick-start-heroku-connect-cli>
- <https://devcenter.heroku.com/articles/heroku-connect-diagnose>
