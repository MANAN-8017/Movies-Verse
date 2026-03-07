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
            old_desc = merged.get("description") or ""
            new_desc = value or ""

            if len(new_desc) > len(old_desc):
                merged["description"] = new_desc

        elif value is not None:
            merged[key] = value

    if old.get("source") == "omdb" and new.get("source") == "tmdb":
        merged["source"] = "tmdb"

    return merged