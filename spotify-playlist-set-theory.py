#!/usr/bin/python3

import argparse
import sys
import os
import webbrowser
import base64
import requests
import re


# client ID is public
CLIENT_ID = 'bd9297adefb44ddfac570814af8aaa05'
access_token = None
username = None


def get_playlist_tracks(playlist_id):
    headers = {'Authorization': 'Bearer ' + access_token}
    # only get the fields we need
    payload = {'fields': 'items(track(id)),next'}

    print("Getting tracks listing for playlist", playlist_id, "...")

    r = requests.get('https://api.spotify.com/v1/users/%s/playlists/%s/tracks' % (username, playlist_id), headers=headers, params=payload)
    print("get_playlist_tracks: HTTP", r.status_code)
    r.raise_for_status()

    json = r.json()
    track_list = [item['track']['id'] for item in json['items']]
    next = json['next']

    # loop until we've retrieved all tracks
    while next and next != 'null':
        r = requests.get(next, headers=headers)
        print('.', end='', flush=True)
        r.raise_for_status()

        json = r.json()
        track_list.extend([item['track']['id'] for item in json['items']])
        next = json['next']

    print("%d tracks in playlist" % len(track_list), playlist_id)

    return track_list


def perform_set_operation_on_playlists(operation, playlist_a, playlist_b):
    # can we use a shortcut?
    if operation == '000':
        return []

    if type(playlist_a) is not list:
        # input param came in as playlist ID
        playlist_a = set(get_playlist_tracks(playlist_a))
    else:
        # input param came in as track listing
        playlist_a = set(playlist_a)

    if type(playlist_b) is not list:
        # input param came in as playlist ID
        playlist_b = set(get_playlist_tracks(playlist_b))
    else:
        # input param came in as track listing
        playlist_b = set(playlist_b)

    if operation == '001':
        return list(playlist_b - playlist_a)
    elif operation == '010':
        return list(playlist_a & playlist_b)
    elif operation == '011':
        return list(playlist_b)
    elif operation == '100':
        return list(playlist_a - playlist_b)
    elif operation == '101':
        return list(playlist_a ^ playlist_b)
    elif operation == '110':
        return list(playlist_a)
    elif operation == '111':
        return list(playlist_a | playlist_b)
    else:
        raise Exception("Invalid operation")


def add_tracks_to_playlist(track_list, output_playlist_id):
    headers = {'Authorization': 'Bearer ' + access_token}

    num_tracks = len(track_list)
    # limit imposed by API
    item_limit = 100

    while num_tracks > 0:
        payload = {'uris': ["spotify:track:%s" % track_id for track_id in track_list[-num_tracks:][:item_limit] if track_id is not None]}

        r = requests.post('https://api.spotify.com/v1/users/%s/playlists/%s/tracks' % (username, output_playlist_id), headers=headers, json=payload)
        print("add_tracks_to_playlist: HTTP", r.status_code)
        r.raise_for_status()

        num_tracks -= item_limit


def remove_tracks_from_playlist(track_list, output_playlist_id):
    headers = {'Authorization': 'Bearer ' + access_token}

    num_tracks = len(track_list)
    # limit imposed by API
    item_limit = 100

    while num_tracks > 0:
        payload = {'tracks': [{"uri": "spotify:track:%s" % track_id} for track_id in track_list[-num_tracks:][:item_limit]]}

        r = requests.delete('https://api.spotify.com/v1/users/%s/playlists/%s/tracks' % (username, output_playlist_id), headers=headers, json=payload)
        print("remove_tracks_from_playlist: HTTP", r.status_code)
        r.raise_for_status()

        num_tracks -= item_limit


def create_parser():
    parser = argparse.ArgumentParser(description='Applies set theory to tracks in Spotify playlists.  Enables populating an output playlist with the mathematical result of two input playlists and a set theory operation (e.g. intersect, union).')

    parser.add_argument('operation', choices=['000', '001', '010', '011', '100', '101', '110', '111', 'intersection', 'symmetric_difference', 'union'], help='The set theory operation to perform on the playlists.  The 3 binary digits together map to the classic overlapping Venn diagram.')
    parser.add_argument('username', help='Spotify username containing the playlists')
    parser.add_argument('input_playlist_id', nargs=2, help='Spotify ID of input playlist')
    parser.add_argument('output_playlist_id', help='Spotify ID of output playlist')

    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    try:
        access_token = os.environ['access_token']
    except KeyError:
        input('After pressing Enter, a new browser tab will launch.  Authorize the Spotify application.  After it redirects you to a nonexistent webpage, copy the "access_token" query parameter in the URL and set it as the "access_token" in your Bash environment before re-running this script.')
        webbrowser.open_new_tab('https://accounts.spotify.com/authorize?client_id=%s&response_type=token&redirect_uri=http://tk5Vc6D835LtapxZIRMtfdWeWrJj5h2B-spotify-playlist-set-theory.com/&scope=playlist-modify-public playlist-modify-private' % CLIENT_ID)
        sys.exit(1)

    username = args.username

    # accept keywords for well-known operations
    if args.operation == 'intersection':
        args.operation = '010'
    elif args.operation == 'symmetric_difference':
        args.operation = '101'
    elif args.operation == 'union':
        args.operation = '111'

    # all operations must map to 3-digit binary string
    if not re.match(r'[01]{3}', args.operation):
        raise Exception("Invalid operation")

    result_tracks = perform_set_operation_on_playlists(args.operation, args.input_playlist_id[0], args.input_playlist_id[1])
    print("Operation %s yielded %d results" % (args.operation, len(result_tracks)))

    output_playlist_tracks = get_playlist_tracks(args.output_playlist_id)

    tracks_to_add = perform_set_operation_on_playlists('100', result_tracks, output_playlist_tracks)
    print("%d tracks to add to playlist" % len(tracks_to_add), args.output_playlist_id, "...")
    add_tracks_to_playlist(tracks_to_add, args.output_playlist_id)

    tracks_to_remove = perform_set_operation_on_playlists('001', result_tracks, output_playlist_tracks)
    print("%d tracks to remove from playlist" % len(tracks_to_remove), args.output_playlist_id, "...")
    remove_tracks_from_playlist(tracks_to_remove, args.output_playlist_id)

    print("Success")
