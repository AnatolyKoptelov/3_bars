import sys
import json
import requests
import argparse
from bars import load_data, load_json


def fetch_web_url(url, get_params):
    response = requests.get(url, params=get_params)
    if response.ok:
        return response.content


def get_args():
    parser = argparse.ArgumentParser(
        description='Bars database updater'
    )
    parser.add_argument(
        'key',
        metavar='key',
        help='{}{}'.format(
            'apidata.mos.ru API key ',
            'Type your key for update your local datafile',
        )
    )
    return parser.parse_args()


def get_actual_version(key, fetch_function, load_data_function):
    url = 'https://apidata.mos.ru/v1/datasets/1796/version'
    get_params = {'api_key': key}
    version_data = load_data_function(fetch_function(url, get_params))
    return '{}.{}'.format(
        version_data['versionNumber'],
        version_data['releaseNumber'],
    )


def get_actual_data(key, fetch_function, load_data_function):
    url = 'https://apidata.mos.ru/v1/features/1796/'
    get_params = {'api_key': key}
    return load_data_function(fetch_function(url, get_params))


def get_local_version(local_data):
    return'{}.{}'.format(
        local_data['features'][0]['properties']['VersionNumber'],
        local_data['features'][0]['properties']['ReleaseNumber'],
    )


def save_to_file(recording_data, path):
    with open(path, 'w') as file_to_write:
        json.dump(
            recording_data,
            file_to_write,
            ensure_ascii=False)


if __name__ == '__main__':
    filepath = './bars.json'
    args = get_args()
    try:
        actual_version = get_actual_version(
            key=args.key,
            fetch_function=fetch_web_url,
            load_data_function=load_json,
        )
    except (requests.exceptions.RequestException, TypeError):
        sys.exit('{}{}{}'.format(
            'Cannot connect to https://apidata.mos.ru/ or your api_key ',
            'is not confirmed. \nCheck this value in your account page:',
            'https://apidata.mos.ru/Account/Manage',
        ))
    try:
        local_data = load_json(load_data(filepath))
        local_version = get_local_version(local_data)
    except (json.decoder.JSONDecodeError, TypeError):
        local_version = None
    if actual_version != local_version:
        actual_data = get_actual_data(
            key=args.key,
            fetch_function=fetch_web_url,
            load_data_function=load_json,
        )
        save_to_file(actual_data, filepath)
        print('{}{}'.format(
            './bars.json',
            ' was successible updated',
        ))
    else:
        print('{}{}'.format(
            './bars.json',
            ' is updated, there nothing to do',
        ))
