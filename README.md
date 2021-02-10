# Shorty

This repository includes a REST API built with Flask.

## How to run the app

In the `shorty` folder, to install all required Python packages from `requirements.txt`, you will
have to do the following:

```bash
pip install --upgrade -r requirements.txt
```

Assign any desired configuration values per environment in `config.{env}.json`, 
where env is the corresponding environment (i.e. for dev environment this will be `config.dev.json`).

Finally, in the `shorty` folder execute the command:

```bash
python run.py {env}
```

Where env is the corresponding environment (i.e. for dev environment the command will be `python run.py dev`)

*edit: the `config.dev.json` file has been deleted, but the needed `generic_access_token` from bitly*
*has been left if the `devops/config.dev.json` file which was intended for the Dockerfile*

## How to run the tests

In order to run the tests, while being in the application directory, enter:

```bash
pytest test
```

The reason behind renaming `tests` to `test` was because of a conflict
with the parsing of the environmental config on initialization,
so this was solved by renaming the directory.

## Usage

### Browser

In order to use the API, you can install [Postman](https://www.postman.com/downloads/)
and enter the endpoint which is:

```
http://localhost:5000/api/shortlinks [POST]
```

To post a successful request to the endpoint, you need to set in the headers section
the `Content-Type` to `application/json` and have a valid request body, which should be in the format:

```json
{
    "provider": string,
    "url": string
}

```

Following that, you will get a Response that should be in the format:

```json
{
    "url": string,
    "link": string
}
```

### Swagger UI

By having the Python application running, you can visit [localhost:5000/api/docs](http://localhost:5000/api/docs),
and try out posting a request in a similar way as the aforemention in the `Browser` section.

There is also a brief explanation of the request, response and their attributes.

*note1: integration tests were not at the desired condition to be committed, so they weren't delivered.*

*note2: the request model, although is not used, was added for possible future use.*