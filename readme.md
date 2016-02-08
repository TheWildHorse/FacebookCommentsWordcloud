# Facebook Page Comment Wordclouds
This two scripts have been created to build wordclouds from facebook comments on page posts. They are really hacky and specific, and you will need to change a few things to make the whole thing work for you.

It contains two folders:  
- facebook_page_comment_scraper  
- wordcloud_generator  


###facebook_page_comment_scraper
PHP CLI tool that fetches the comments from the page.
To get started, run composer install to install the FB SDK and other dependencies. Open the `scrapeCLI.php` file and fill the FB app config with your FB app creditentials. These are used to authenticate to facebook and scrape the comments.  

This CLI implements two commands: `getTargetPosts` and `processPosts`
And the general usage looks like this:  
`php scrapeCLI.php [getTargetPosts|processPosts] -i {FB page ID} -f {filename for results}`

First you have to use the `getTargetPosts` command to fetch the post IDs we will later scrape. Use the `-i` flag to set the FB page id, and the `-f` to set the filename the data will be saved in. To fetch the posts, run the `processPosts` command with the same parameters. A file will be created containing all comments found. You can use that in the next step - creating the wordcloud.

###wordcloud_generator
This python script utilizes [this word_cloud Python library](https://github.com/amueller/word_cloud), please advise that page on installation procedure.

To use the script, place the `[SOURCE_NAME]_comments.txt` and `[SOURCE_NAME].png` files in the script folder where the [SOURCE_NAME] is the identifier you set for that cloud. That source name has to be written inside of `script.py` sourceNames array. It will then use them to find above files by that source name and generate the clound when the script is ran.

The `script.py` file also contains a stopwords array which includes all words that should be ignored when creating a word cloud, it currently contains some Croatian stopwords and extra words I added to get better results. You will probably have to change those or add more to get the best results.