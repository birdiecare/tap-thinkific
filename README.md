# tap-thinkific

This repo contains a Singer "tap" for downloading data from www.thinkific.com. The tap conforms to the Singer specification and can be used standalone or with Meltano (recommended) to send data to wide variety of destinations for analysis. See here for a list of Meltano destinations: https://hub.meltano.com/loaders/.

The tap is built with the [Meltano Tap SDK](https://sdk.meltano.com).

## Supported Streams

The tap currently downloads data from these endpoints:
- [/courses](https://developers.thinkific.com/api/api-documentation/#/Courses/getCourses)
- [/enrollments](https://developers.thinkific.com/api/api-documentation/#/Enrollments/getEnrollments)

A full list of thinkific endpoints is available at https://developers.thinkific.com/api/api-documentation. Please submit an issue to request other endpoints or feel free to open up a PR.

## Installation

#### Pip 
This tap isn't currently published on PyPi. You can install directly with

```bash
pipx install git+https://github.com/birdiecare/tap-thinkific.git
```

#### Meltano
Similarly this tap isn't available on the meltano hub yet. You can still install it directly with 

```bash
meltano add --custom extractor tap-thinkific
```
...and specifying `git+https://github.com/birdiecare/tap-thinkific.git` as the pip URL.

## Configuration

The tap takes three configuration inputs:

```json
{
    "api_key": "<your_thinkific_api_key>",
    "subdomain": "<your_thinkific_subdomain",
    "start_date": "2022-01-18T00:00:00Z"
}
```

Only enrollments created or updated after the `start_date` will be downloaded. The `subdomain` and `api_key` are obtained from your Thinkific settings. See here for instructions: https://developers.thinkific.com/api/api-key-auth


## Usage

You can test the tap by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-thinkific --version
tap-thinkific --help
tap-thinkific --config CONFIG --discover > ./catalog.json
```

See https://www.singer.io/#what-it-is for more info on running singer taps and targets.
