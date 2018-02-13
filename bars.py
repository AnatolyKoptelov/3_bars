import sys
import json
import argparse
from geopy.distance import vincenty


def get_args():
    parser = argparse.ArgumentParser(
        description='Bars information'
    )
    parser.add_argument(
        'path',
        metavar='path',
        type=argparse.FileType('rb'),
        help='Path of file with data',
    ),
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
        ),
    )
    return parser.parse_args()


def get_biggest_bar_data(bars_data):
    return {
        'The biggest bar': max(
            bars_data,
            key=lambda bar: bar['SeatsCount'],
        ),
    }


def get_smallest_bar_data(bars_data):
    return {
        'The smallest bar': min(
            bars_data,
            key=lambda bar: bar['SeatsCount'],
        ),
    }


def get_distance(latitude, longitude, actual_latitude, actual_longitude):
    return vincenty(
        (latitude, longitude),
        (actual_latitude, actual_longitude),
    ).km


def get_closest_bar_data(*args):
    bars_data, latitude, longitude, get_distance_function = args[0]
    return {
        'The closest bar': min(
            bars_data,
            key=lambda bar: get_distance_function(
                latitude=bar['Latitude_WGS84'],
                longitude=bar['Longitude_WGS84'],
                actual_latitude=latitude,
                actual_longitude=longitude,
            )
        ),
    }


def bar_for_print(bar_data):
    return ['{}:\n\t{}\t{}\n\t{}\t{}\n\t{}\t{}'.format(
        title,
        'Bar Name: ',
        bar['Name'],
        'Address:',
        bar['Address'],
        'SeatsCount: ',
        bar['SeatsCount'],
    ) for title, bar in bar_data.items()][0]


def check_args(args):
    if len(sys.argv) == 2:
        sys.exit('Enter any optional parameter for view bar info ')
    if args.close and (args.latitude is None or args.longitude is None):
        sys.exit('{}{}'.format(
            'For getting the closest bar ',
            'latitude and longitude options are required',
        ))


if __name__ == '__main__':
    args = get_args()
    check_args(args)
    try:
        bars_data = json.loads(
            args.path.read().decode('cp1251'),
            encoding='utf-8',
        )
        attributes = [
            (args.big, get_biggest_bar_data, bars_data),
            (args.small, get_smallest_bar_data, bars_data),
            (args.close,
             get_closest_bar_data,
             (
                bars_data,
                args.latitude,
                args.longitude,
                get_distance,
             )),
        ]
        for option, function, arguments in attributes:
            if option:
                print(bar_for_print(function(arguments)))
    except (json.decoder.JSONDecodeError, TypeError):
        print('{}{}\n{}{}'.format(
            'Cannot open the file: ',
            args.path.name,
            'Download actual version from: ',
            'https://data.mos.ru/opendata/7710881420-bary',
        ))
