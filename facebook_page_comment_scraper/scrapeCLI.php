<?php
ini_set('memory_limit','256M');
date_default_timezone_set('Europe/Zagreb');
require('vendor/autoload.php');

// FaceBook app config
$fb = new Facebook\Facebook([
  'app_id' => '',
  'app_secret' => '',
  'default_graph_version' => 'v2.5',
  'default_access_token' => '',
]);


// === CLI TOOL SETUP ===
$cmd = new Commando\Command();

$cmd->setHelp(
	'Gets comments for the latest posts on a Facebook page.' . PHP_EOL .
	'Usage: CMD [getTargetPosts|processPosts] -i {FB page ID} -f {filename for results}');

$cmd->option()
    ->require()
    ->describedAs('Which function should I do')
    ->must(function($function) {
        $functions = array('getTargetPosts', 'processPosts');
        return in_array($function, $functions);
    });

$cmd->option('i')
	->aka('fbpageid')
    ->require()
    ->describedAs('ID of the Facebook page');

$cmd->option('f')
    ->aka('filename')
    ->require()
    ->describedAs('File name that the result will be saved in, no extension');

// === APP LOGIC ===

// Fetches post IDs that will be scraped for comments
function getTargetPosts($app, $FBPageID) {
	$posts = [];
	$response = $app->get('/' . $FBPageID . '/posts?limit=100');
	$response = $response->getGraphEdge();
	for($i = 0; $i < 50; $i++) {
		foreach ($response as $post) {
			$posts[] = $post->asArray()['id'];
		}
		$response = $app->next($response);
	}
	return $posts;
}

function fetchCommentsFromPosts($app, $FBPageID, $filename) {
	$posts = file_get_contents($filename . '_post_ids.txt');
	$posts = explode(PHP_EOL, $posts);
	$queries = [];
	$comments = [];

	foreach($posts as $postId) {
		$queries[] = ['method' => 'GET', 'relative_url' => '/'.$postId.'/comments?limit=20000'];
		// If batch is filled, process it
		if(count($queries) == 50 || count($queries) == count($posts)) {
			$request = $app->request('POST', '?batch='.json_encode($queries));
			try {
				$batchResponse = $app->getClient()->sendRequest($request);
			} catch(Facebook\Exceptions\FacebookResponseException $e) {
				// When Graph returns an error
				echo "\033[31m Graph returned an error: " . $e->getMessage() . "\033[0m" . PHP_EOL;
				echo "Stored progress, exiting program." . PHP_EOL;
				file_put_contents($filename . '_post_ids.txt', implode(PHP_EOL, $posts));
				file_put_contents($filename . '_comments.txt', implode(PHP_EOL, $comments), FILE_APPEND);
				return null;
			} catch(Facebook\Exceptions\FacebookSDKException $e) {
				// When validation fails or other local issues
				echo "\033[31m Facebook SDK returned an error: " . $e->getMessage() . "\033[0m" . PHP_EOL;
				echo "Stored progress, exiting program." . PHP_EOL;
				file_put_contents($filename . '_post_ids.txt', implode(PHP_EOL, $posts));
				file_put_contents($filename . '_comments.txt', implode(PHP_EOL, $comments), FILE_APPEND);
				return null;
			}
			foreach($batchResponse->getDecodedBody() as $response) {
				$commentsData = json_decode($response['body'], true);
				foreach ($commentsData['data'] as $commentData) {
					$comments[] = $commentData['message'];
				}
			}
			$posts = array_slice($posts, 50);
			echo "Batch completed, remaining posts to process: " . count($posts) . " Comments found:" . count($comments) . PHP_EOL;
			$queries = [];
		}
	}
	file_put_contents($filename . '_post_ids.txt', implode(PHP_EOL, $posts));
	file_put_contents($filename . '_comments.txt', implode(PHP_EOL, $comments), FILE_APPEND);
}


// Handle different functionalities
switch($cmd[0]) {
	case 'getTargetPosts';
		print "Fetching post IDs for FB page " . $cmd['fbpageid'] . PHP_EOL;
		$posts = getTargetPosts($fb, $cmd['fbpageid']);
		file_put_contents($cmd['filename'] . '_post_ids.txt', implode(PHP_EOL, $posts));
		print "Page IDs written to " . $cmd['filename'] . '_post_ids.txt' . PHP_EOL;
		print "To start processing them, run processPosts command with the same arguments." . PHP_EOL;
		break;
	case 'processPosts';
		fetchCommentsFromPosts($fb, $cmd['fbpageid'], $cmd['filename']);
		break;
}

