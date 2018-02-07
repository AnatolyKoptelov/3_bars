import os
import sys
import json
import argparse


def load_data(filepath):
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as file_to_read:
            return file_to_read.read()


def get_args():
    parser = argparse.ArgumentParser(
        description='Bars information'
    )
    parser.add_argument(
        '-b',
        '--big',
        action='store_true',
        help='View information of the biggest bar',
    )
    parser.add_argument(
        '-s',
        '--small',
        action='store_true',
        help='View information of the smallest bar',
    )
    parser.add_argument(
        '-c',
        '--close',
        action='store_true',
        help='View information of the closest bar',
    )
    parser.add_argument(
        '-lat',
        '--latitude',
        type=float,
        help='{}{}'.format(
            'Type your actual latitude in DD.DDDDD ',
            'format for getting the closest bar',
        )
    )
    parser.add_argument(
        '-lon',
        '--longitude',
        type=float,
        help='{}{}'.format(
            'Type your actual longitude in DD.DDDDD ',
            'format for getting the closest bar',
        )
    )
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.error('Enter any option parameter for view bar info ')
    if args.close and (args.latitude is None or args.longitude is None):
        parser.error('{}{}'.format(
            'For getting the closest bar ',
            'latitude and longitude options are required',
        ))
    return parser.parse_args()


def load_json(json_file):
    return json.loads(json_file, encoding='utf-8')


def get_biggest_bar(bars_data):
    return {
        'The biggest bar': max(
            bars_data['features'],
            key=lambda bar: bar['properties']['Attributes']['SeatsCount'],
        ),
    }


def get_smallest_bar(bars_data):
    return {
        'The smallest bar': min(
            bars_data['features'],
            key=lambda bar: bar['properties']['Attributes']['SeatsCount'],
        ),
    }


def get_distance(latitude, longitude, actual_latitude, actual_longitude):
    return pow(
        pow(latitude-actual_latitude, 2) + pow(longitude-actual_longitude, 2),
        0.5,
    )


def get_closest_bar(*args):
    bars_data, latitude, longitude, get_distance_function = args[0]
    return {
        'The closest bar': min(
            bars_data['features'],
            key=lambda bar: get_distance_function(
                latitude=bar['geometry']['coordinates'][0],
                longitude=bar['geometry']['coordinates'][1],
                actual_latitude=latitude,
                actual_longitude=longitude,
            )
        ),
    }


def bar_for_print(bar_data):
    return ['{}:\n\t{}\t{}\n\t{}\t{}\n\t{}\t{}'.format(
        title,
        'Bar Name: ',
        bar['properties']['Attributes']['Name'],
        'Address:',
        bar['properties']['Attributes']['Address'],
        'SeatsCount: ',
        bar['properties']['Attributes']['SeatsCount'],
    ) for title, bar in bar_data.items()][0]


if __name__ == '__main__':
    args = get_args()
    filepath = './bars.json'
    try:
        bars_data = load_json(load_data(filepath))
        attributes = [
            (args.big, get_biggest_bar, bars_data),
            (args.small, get_smallest_bar, bars_data),
            (args.close,
             get_closest_bar,
             (
                bars_data,
                args.latitude,
                args.longitude,
                get_distance,
             )),
        ]
        for option, function, arguments in attributes:
            print(option and bar_for_print(function(arguments)) or '')
    except (json.decoder.JSONDecodeError, TypeError):
        print('{}{}{}'.format(
            'Cannot open the file: ',
            filepath,
            ' You can get actual version with update_bars_data.py',
        ))
