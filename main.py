import sys
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBxpv6hMnANDf6srskR0QFaUw1X5-Aa0c8"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

SEARCH_WORD="Hello world"

#linkList.txt file location.
FILENAME="textfile\\store\\location\\linkList.txt"

videos = []
nextPageToken = ""

def youtube_search(options , nextPageToken):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
	
	# Call the search.list method to retrieve results matching the specified
	# query term.
	search_response = youtube.search().list(
	q=options.q,
	part="id,snippet",
	maxResults=options.max_results,
	pageToken=nextPageToken,
	type="video",
	videoDuration="short"
	).execute()
	
	

	# Add each result to the appropriate list, and then display the lists of
	# matching videos, channels, and playlists.
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			videos.append("http://www.youtube.com/watch?v=" + search_result["id"]["videoId"])
	return search_response.get("nextPageToken") ;
	


if __name__ == "__main__":
	argparser.add_argument("--q", help="Search term", default=SEARCH_WORD)
	argparser.add_argument("--max-results", help="Max results", default=50)
	args = argparser.parse_args()
	try:
		for x in range(0, 10):
			nextPageToken = youtube_search(args , nextPageToken)
	except (HttpError, e):
		print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
	
	#Storing the default output stream for the print function
	orig_stdout = sys.stdout
	target = open(FILENAME, 'w')
	target.truncate()
	#Redirecting the print output to the text file
	sys.stdout= target
	print(videos)
	#Putting stuff back the way I found them
	sys.stdout = orig_stdout
	target.close()	