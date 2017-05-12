# spotify-playlist-set-theory
Applies set theory to tracks in Spotify playlists.  Enables populating a destination playlist with the mathematical result of two input playlists and a set theory operation (e.g. intersect, union).


# Operation
Inputs:
* ID of two Spotify playlists.  These playlists are not modified.
* Spotify username containing those playlists
* Operation
    * 000 = null set
    * 001 = B - A
    * 010 = intersection = Intersect
    * 011 = B
    * 100 = A - B
    * 101 = symmetric_difference
    * 110 = A
    * 111 = union

Output:
* ID of destination Spotify playlist.  This playlist is modified to match the result of the set theory operation.  Playlist must already exist (but allowed to be empty).


# Features
* Leverages Spotify Web API v1 with [Implicit Grant Flow](https://developer.spotify.com/web-api/authorization-guide/#implicit_grant_flow)
* Abstracts away batch limits (100 items, usually)
* Performs deduplication to prevent unnecessary API requests


# Usage
```
usage: spotify-playlist-set-theory.py [-h]
                                      {000,001,010,011,100,101,110,111,intersection,symmetric_difference,union}
                                      username input_playlist_id
                                      input_playlist_id output_playlist_id

Applies set theory to tracks in Spotify playlists. Enables populating an
output playlist with the mathematical result of two input playlists and a set
theory operation (e.g. intersect, union).

positional arguments:
  {000,001,010,011,100,101,110,111,intersection,symmetric_difference,union}
                        The set theory operation to perform on the playlists.
                        The 3 binary digits together map to the classic
                        overlapping Venn diagram.
  username              Spotify username containing the playlists
  input_playlist_id     Spotify ID of input playlist
  output_playlist_id    Spotify ID of output playlist

optional arguments:
  -h, --help            show this help message and exit
```


# Example
```
user@computer:~$ ./spotify-playlist-set-theory.py 010 jelchison 5UYwlMnNTLqRuJ0CxUutOD 4EBTp2BrFqkv2123Zzbfsj 5NoLdcuoI3xdV52jqna4jY
After pressing Enter, a new browser tab will launch.  Authorize the Spotify application.  After it
redirects you to a nonexistent webpage, copy the "access_token" query parameter in the URL and set it
as the ACCESS_TOKEN in your Bash environment before re-running this script.

user@computer:~$ ACCESS_TOKEN=BQCO...<truncated>...soXw ./spotify-playlist-set-theory.py intersection jelchison 5UYwlMnNTLqRuJ0CxUutOD 4EBTp2BrFqkv2123Zzbfsj 5NoLdcuoI3xdV52jqna4jY
Getting tracks listing for playlist 5UYwlMnNTLqRuJ0CxUutOD ...
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
979 tracks in playlist 5UYwlMnNTLqRuJ0CxUutOD
Getting tracks listing for playlist 4EBTp2BrFqkv2123Zzbfsj ...
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
get_playlist_tracks: HTTP 200
2586 tracks in playlist 4EBTp2BrFqkv2123Zzbfsj
Operation 010 yielded 405 results
Getting tracks listing for playlist 5NoLdcuoI3xdV52jqna4jY ...
get_playlist_tracks: HTTP 200
3 tracks in playlist 5NoLdcuoI3xdV52jqna4jY
402 tracks to add to playlist 5NoLdcuoI3xdV52jqna4jY ...
add_tracks_to_playlist: HTTP 201
add_tracks_to_playlist: HTTP 201
add_tracks_to_playlist: HTTP 201
add_tracks_to_playlist: HTTP 201
add_tracks_to_playlist: HTTP 201
0 tracks to remove from playlist 5NoLdcuoI3xdV52jqna4jY ...
Success
```


# Prerequisites
* Python 2.7
* requests


# Tips
* Since this application uses the [Implicit Grant Flow](https://developer.spotify.com/web-api/authorization-guide/#implicit_grant_flow), there's no need to register your own Spotify application
* [Playlist IDs](https://developer.spotify.com/web-api/user-guide/#spotify-uris-and-ids) can be found using your Spotify desktop client
