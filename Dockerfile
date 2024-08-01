FROM meltano/meltano:v3.4.2-python3.11

ARG SNOWFLAKE_ANALYTICS_SINGER_USER_PASSWORD

WORKDIR /usr/src/meltano


# initialise project
RUN meltano init analytics_integrations
WORKDIR /usr/src/meltano/analytics_integrations

# copy config details for extractor and loader and script for running pipeline.
COPY mypy.ini pyproject.toml tox.ini meltano.yml logging.yml ./
COPY ./tap_thinkific /usr/src/meltano/analytics_integrations/tap_thinkific

RUN meltano add extractor tap-thinkific --variant=birdiecare
RUN printf 'target_snowflake\ngit+https://github.com/augusthorlen0/pipelinewise-target-snowflake.git@be0a09ecfd97bcbf28d3488df5e5364a743ce768\target-snowflake\ncatalogue,state\n\n' | meltano add --custom loader target-snowflake
# RUN meltano install

RUN meltano lock --update --all