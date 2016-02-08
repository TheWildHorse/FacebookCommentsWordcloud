# -*- coding: utf-8 -*-

from os import path
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator

d = path.dirname(__file__)

stopwordsHR = ['a', 'ako', 'ali', 'bi', 'bih', 'bila', 'bili', 'bilo', 'bio',
'bismo', 'biste', 'biti', 'bumo', 'da', 'do', 'duž', 'ga', 'hoće', 'hoćemo',
'hoćete', 'hoćeš', 'hoću', 'i', 'iako', 'ih', 'ili', 'iz', 'ja', 'je',
'jedna', 'jedne', 'jedno', 'jer', 'jesam', 'jesi', 'jesmo', 'jest', 'jeste',
'jesu', 'jim', 'joj', 'još', 'ju', 'kada', 'kako', 'kao', 'koja', 'koje',
'koji', 'kojima', 'koju', 'kroz','li', 'me', 'mene', 'meni', 'mi', 'mimo',
'moj', 'moja', 'moje', 'mu', 'na', 'nad', 'nakon', 'nam', 'nama', 'nas',
'naš', 'naša', 'naše', 'našeg', 'ne', 'nego', 'neka', 'neki', 'nekog', 'neku',
'nema', 'netko', 'neće', 'nećemo', 'nećete', 'nećeš', 'neću', 'nešto', 'ni',
'nije', 'nikoga', 'nikoje', 'nikoju', 'nisam', 'nisi', 'nismo', 'niste',
'nisu', 'njega', 'njegov', 'njegova', 'njegovo', 'njemu', 'njezin', 'njezina',
'njezino', 'njih', 'njihov', 'njihova', 'njihovo', 'njim', 'njima', 'njoj',
'nju', 'no', 'o', 'od', 'odmah', 'on', 'ona', 'oni', 'ono', 'ova', 'pa',
'pak', 'po', 'pod', 'pored', 'prije', 's', 'sa', 'sam', 'samo', 'se', 'sebe',
'sebi', 'si', 'smo', 'ste', 'su', 'sve', 'svi', 'svog', 'svoj', 'svoja',
'svoje', 'svom', 'ta', 'tada', 'taj', 'tako', 'te', 'tebe', 'tebi', 'ti',
'to', 'toj', 'tome', 'tu', 'tvoj', 'tvoja', 'tvoje', 'u', 'uz', 'vam', 'vama',
'vas', 'vaš', 'vaša', 'vaše', 'već', 'vi', 'vrlo', 'za', 'zar', 'će', 'ćemo',
'ćete', 'ćeš', 'ću', 'što', 'e', 'ima', 'ce', 'kad', 'sad', 'sto', 'ovo',
'onda', 'ma', 'zato', 'ko', 'jo', 'tko', 'im', 'gdje', 'sta', 'šta', 'bez',
'jos', 'kod', 'ovaj', 'treba', 'nek', 'vise', 'zasto', 'al', 'ono', 'dok', 'mogu',
'ove', 'tamo', 'neko', 'jako', 'jel', 'zbog', 'nebi', 'http', 'ovi', 'ove', 'one',
'on', 'https', 'kaj', 'svaka', 'niti', 'u', 'kakva', 'oko', 'ovu', 'niko', 'di',
'onaj', 'nesto', 'com', 'neke', 'imam', 'ide', 'eto', 'imamo', 'isto', 'ide', 'tak',
'preko', 'bit', 'baš', 'tom', 'tek', 'ipak', 'bar', 'www', 'netko', 'cu', ]

# Sources - contains the names of sources to process
# To be able to process a source we need two files:
# [SOURCE_NAME]_comments.txt - the file used as a source for the wordcloud
# [SOURCE_NAME].png - Image that the wordcloud will be shaped/colored into
sourceNames = []

for sourceName in sourceNames:
	# Read the whole text.
	text = open(path.join(d, sourceName + '_comments.txt')).read()
	coloring = imread(path.join(d, sourceName + ".png"))

	# Generate a word cloud image 
	wordcloud = WordCloud(
		mask=coloring,
		font_path='/Users/igorrinkovec/Library/Fonts/LobsterTwo-Regular.otf',
		relative_scaling=.5,
		background_color="white",
		width=3000,
		height=3000,
		stopwords=stopwordsHR).generate(text)
	image_colors = ImageColorGenerator(coloring)

	# Display the generated image:
	# the matplotlib way:
	import matplotlib.pyplot as plt
	plt.imshow(wordcloud.recolor(color_func=image_colors))
	plt.axis("off")
	fig = plt.gcf();
	fig.set_size_inches(30, 30)
	fig.savefig(sourceName + '_cloud.png', dpi=100)
