# Deploy to Snowflake Snowpark Container Services

This demo shows how to develop, build and deploy to Snowflake Snowpark Container Services using Dagger.

This repository shows a simple development environment, ready to use and is made for being forked, modified and extended for your own use.

## Requirements

- [Install Dagger](https://docs.dagger.io/install)
- Have basic knowledge of Snowflake's Snowpark Container Services ([first tutorial](https://docs.snowflake.com/en/developer-guide/snowpark-container-services/tutorials/tutorial-1))

## Setup

Create a `config.toml` with your Snowflake credentials:

```
cp config.sample.toml config.toml
```

Edit the file with your own info.

This demo assumes you already have provisioned a first Compute pool and the `echo_service` SERVICE and `my_echo_udf` FUNCTION from the Snowpark tutorial.

> **_NOTE:_** You can extend the demo from the current code to provision everything from the Dagger pipeline without using the Snowflake Snowsight UI.
