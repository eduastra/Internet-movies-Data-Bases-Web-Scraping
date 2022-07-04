from imdb import IMDb

ia=IMDb()
#dp = ia.get_movie('4574334')
#print(dp.keys())
#print(dp.get('writer'))
print(dir(ia))
"""
['localized title', 'cast', 'genres', 'runtimes', 'countries', 'country codes',
 'language codes', 'color info', 'aspect ratio', 'sound mix', 'box office', 'certificates',
 'original air date', 'rating', 'votes', 'cover url', 'imdbID', 'plot outline', 'languages', 
 'title', 'year', 'kind', 'original title', 'director', 'writer', 'producer', 'composer', 
 'cinematographer', 'editor', 'editorial department', 'casting director', 'production design', 
 'art direction', 'set decoration', 'costume designer', 'make up', 'production manager', 
 'assistant director', 'art department', 'sound crew', 'special effects', 'visual effects',
  'stunt performer', 'camera and electrical department', 'animation department', 'casting department',
   'costume department', 'location management', 'music department', 'script department', 
   'transportation department', 'miscellaneous crew', 'thanks', 'akas', 'production companies',
    'distributors', 'special effects companies', 'other companies', 'plot', 'synopsis', 
    'canonical title', 'long imdb title', 'long imdb canonical title', 'smart canonical title', 
    'smart long imdb canonical title', 'full-size cover url']
"""