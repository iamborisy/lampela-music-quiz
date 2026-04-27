#!/usr/bin/env python3
"""
Script to update tracks.json from list.txt file.

Expected format in list.txt:
Genre
Decade
Subgenre
Track Title
Full URL to YouTube Music
Track Title
Full URL to YouTube Music
...

Example:
Blues
1920-1940
Countryblues
Charley Patton: Down the Dirt Road Blues
https://music.youtube.com/watch?v=fzcCQJ3F_eQ&si=RMjYVOlHkLclHmTo
Tommy Johnson: Canned Heat Blues
https://music.youtube.com/watch?v=RHw1ugBLS5g
"""

import argparse
import json
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs


def extract_youtube_id(url):
    """Extract YouTube video ID from full URL."""
    try:
        parsed_url = urlparse(url)
        # Extract 'v' parameter from query string
        video_id = parse_qs(parsed_url.query).get('v', [None])[0]
        if video_id:
            return video_id
        # Fallback: check if it's already just an ID
        if len(url) == 11 and url.isalnum():
            return url
        return None
    except Exception:
        return None


def load_existing_tracks():
    """Load existing tracks from tracks.json."""
    if os.path.exists("tracks.json"):
        with open("tracks.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tracks(tracks):
    """Save tracks to tracks.json."""
    with open("tracks.json", "w") as f:
        json.dump(tracks, f, indent=2)
    print(f"✓ Saved {len(tracks)} tracks to tracks.json")


def is_duplicate(new_track, existing_tracks):
    """Check if track already exists by title and URL."""
    for track in existing_tracks:
        if (track.get("title") == new_track.get("title") and
            track.get("youtube") == new_track.get("youtube")):
            return True
    return False


def parse_list_txt(path):
    """Parse list.txt and return list of new tracks."""
    path = Path(path)
    if not path.exists():
        print(f"❌ Error: {path} not found")
        return []

    new_tracks = []

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    i = 0
    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Check if this is a genre line (followed by decade and subgenre)
        if i + 2 < len(lines) and lines[i+1] and lines[i+2]:
            # This might be genre/decade/subgenre block
            genre = line
            decade = lines[i + 1]
            subgenre = lines[i + 2]

            i += 3

            # Now collect all title-url pairs for this genre
            while i < len(lines):
                if not lines[i]:  # Empty line
                    i += 1
                    continue

                # Check if next line is a URL (genre line starts differently)
                if i + 1 < len(lines) and lines[i + 1].startswith("http"):
                    title = lines[i].lstrip("- ")
                    url_line = lines[i + 1]
                    youtube_id = extract_youtube_id(url_line)

                    if youtube_id:
                        track = {
                            "title": title,
                            "youtube": youtube_id,
                            "genre": genre,
                            "subgenre": subgenre,
                            "decade": decade
                        }
                        new_tracks.append(track)
                        print(f"  ✓ Parsed: {title}")
                    else:
                        print(f"  ⚠ Could not extract YouTube ID from: {url_line}")

                    i += 2
                else:
                    # Not a URL pair, must be a new genre block
                    break
        else:
            i += 1

    return new_tracks


def main(args):
    print("🎵 Music Quiz Database Updater")
    print("=" * 50)

    # Parse new tracks from list.txt
    input_path = args.file
    if input_path is None:
        default_path = Path("list.txt")
        if default_path.exists():
            input_path = default_path
        else:
            alt_path = Path("templates/list.txt")
            if alt_path.exists():
                input_path = alt_path
    if input_path is None:
        print("❌ Error: no list.txt file found in project root or templates/")
        return

    print(f"\n📖 Parsing {input_path}...")
    new_tracks = parse_list_txt(input_path)

    if not new_tracks:
        print("❌ No tracks found in list.txt")
        return

    print(f"\n✓ Found {len(new_tracks)} tracks in list.txt")

    # Load existing tracks
    existing_tracks = load_existing_tracks()
    print(f"📊 Currently have {len(existing_tracks)} tracks in database")

    added_count = 0
    duplicate_count = 0
    if args.overwrite:
        print("\n🔄 Overwrite mode: rebuilding tracks.json from list file")
        existing_tracks = []
        seen = set()
        for track in new_tracks:
            key = (track["title"], track["youtube"])
            if key in seen:
                print(f"  ⊘ Duplicate in list: {track['title']}")
                duplicate_count += 1
                continue
            existing_tracks.append(track)
            seen.add(key)
            print(f"  ✓ Added: {track['title']}")
            added_count += 1
    else:
        print("\n🔍 Checking for duplicates...")
        for track in new_tracks:
            if is_duplicate(track, existing_tracks):
                print(f"  ⊘ Duplicate: {track['title']}")
                duplicate_count += 1
            else:
                existing_tracks.append(track)
                print(f"  ✓ Added: {track['title']}")
                added_count += 1

    # Save updated database
    print("\n💾 Updating database...")
    save_tracks(existing_tracks)

    # Print summary
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"  • New tracks added: {added_count}")
    print(f"  • Duplicates skipped: {duplicate_count}")
    print(f"  • Total tracks in database: {len(existing_tracks)}")
    print("=" * 50)


def parse_args():
    parser = argparse.ArgumentParser(description="Update tracks.json from a list.txt file.")
    parser.add_argument("--file", help="Path to list.txt file")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite tracks.json instead of appending")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
