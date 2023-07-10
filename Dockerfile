FROM meltano/meltano:v2.1.0-python3.7

ARG SNOWFLAKE_ANALYTICS_SINGER_USER_PASSWORD

WORKDIR /usr/src/meltano


# initialise project
RUN meltano init analytics_integrations
WORKDIR /usr/src/meltano/analytics_integrations

# copy config details for extractor and loader and script for running pipeline.
COPY mypy.ini pyproject.toml tox.ini meltano.yml logging.yml ./
COPY ./tap_thinkific /usr/src/meltano/analytics_integrations/tap_thinkific

RUN meltano install