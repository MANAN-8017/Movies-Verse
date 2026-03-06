from django.core.cache import cache

def clean(value):
    if not value or value == "N/A":
        return None
    return value

def merge_movie_data(old, new):

    if not old:
        return new

    merged = old.copy()

    for key, value in new.items():
        if key == "description":
            old_desc = merged.get("description", "")
            new_desc = value or ""

            if len(new_desc) > len(old_desc):
                merged["description"] = new_desc
                
        elif old.get('source') == 'omdb' and new.get('source') == 'tmdb':
            merged['source'] = 'tmdb'

        elif value and not merged.get(key):
            merged[key] = value

    return merged

def update_movie_cache(imdb_id, new_data):
    if imdb_id in cache:
        cache[imdb_id] = merge_movie_data(cache[imdb_id], new_data)
    else:
        cache[imdb_id] = new_data

    return cache[imdb_id]