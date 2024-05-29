"""A generated module for SnowflakeScs functions

This module has been generated via dagger init and serves as a reference to
basic module structure as you get started with Dagger.

Two functions have been pre-created. You can modify, delete, or add to them,
as needed. They demonstrate usage of arguments and return types using simple
echo and grep commands. The functions can be called from the dagger CLI or
from one of the SDKs.

The first line in this comment block is a short description line and the
rest is a long description with more detail on the module's purpose or usage,
if appropriate. All modules should have a short description.
"""

import json

import dagger
from dagger import dag, function, object_type


@object_type
class SnowflakeScs:
    @function
    async def build(self) -> str:
        """Builds a container image, publishes to the registry, and returns the image ref"""

        # Build the container image from the App directory
        source = dag.current_module().source().directory("Tutorial-1")

        target = "fumlyhg-zkb80860.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/my_echo_service_image:latest"
        ctr = source.docker_build(platform=dagger.Platform("linux/amd64"))
        return await ctr.publish(target)

    @function
    async def deploy(self, config: dagger.Secret) -> str:
        """Builds the container from the App code and deploy it to the Container Service"""

        image_ref = await self.build()
        # Extract the image id from the image ref
        image_id = "/" + "/".join(image_ref.split("/")[1:])

        sql_query = f"""
            -- use the test_role and tutorial_db
            USE ROLE test_role;
            USE DATABASE tutorial_db;
            USE SCHEMA data_schema;
            USE WAREHOUSE tutorial_warehouse;

            -- update the service to use the new image
            ALTER SERVICE echo_service
            FROM SPECIFICATION $$
              spec:
                containers:
                - name: echo
                  image: {image_id}
                  env:
                    SERVER_PORT: 8000
                    CHARACTER_NAME: Bob
                  readinessProbe:
                    port: 8000
                    path: /healthcheck
                endpoints:
                - name: echoendpoint
                  port: 8000
                  public: true
                $$;
            """

        snow = dag.snowflake_cli()
        return await snow.query(config, query=sql_query, cache=False)

    @function
    async def url(self, config: dagger.Secret) -> str:
        """Return the URL of the deployed service's endpoint"""
        sql_query = """
            -- use the test_role and tutorial_db
            USE ROLE test_role;
            USE DATABASE tutorial_db;
            USE SCHEMA data_schema;
            USE WAREHOUSE tutorial_warehouse;

            -- get the service endpoint
            SHOW ENDPOINTS IN SERVICE echo_service;
            """

        snow = dag.snowflake_cli()
        resp = await snow.query(config, query=sql_query, format_json=True)
        resp = json.loads(resp)

        endpoints = resp[-1]
        for endpoint in endpoints:
            if endpoint["name"] == "echoendpoint":
                hostname = endpoint["ingress_url"]
                return f"https://{hostname}/ui"

        raise Exception("Endpoint not found")

    @function
    async def echo(self, config: dagger.Secret, input: str) -> str:
        """Call the deployed Echo function and prints the result"""
        sql_query = f"""
            -- use the test_role and tutorial_db
            USE ROLE test_role;
            USE DATABASE tutorial_db;
            USE SCHEMA data_schema;
            USE WAREHOUSE tutorial_warehouse;

            -- get the service endpoint
            SELECT my_echo_udf('{input}');
            """

        snow = dag.snowflake_cli()
        resp = await snow.query(config, query=sql_query, format_json=True, cache=False)
        resp = json.loads(resp)

        # Get the return value from the function call
        return list(resp[-1][0].values())[0]
