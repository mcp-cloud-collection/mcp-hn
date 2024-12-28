import requests
from typing import List, Dict, Union, Any

BASE_API_URL = "http://hn.algolia.com/api/v1"
DEFAULT_NUM_STORIES = 10

# TODO: Update this to be user configurable
DEFAULT_NUM_COMMENTS = 10
DEFAULT_COMMENT_DEPTH = 2

def _validate_comments_is_list_of_dicts(comments: List[Any]) -> bool:
    """
    If the comments is a list of ints, we return False, since we need to get the story info to get the comments.
    """
    return not isinstance(comments[0], int)

def _get_story_info(story_id: int) -> Dict:
    """
    Returns a dictionary with the story info.
    """
    url = f"{BASE_API_URL}/items/{story_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def _format_story_details(story: Union[Dict, int], basic: bool = True) -> Dict:
    """
    Returns a dictionary with the following details:
    {
        "id": int,
        "title": str,
        "url": str,
        "author": str,
        "points": int (nullable),
        "comments": List[Dict]
    }

    If basic is False, then the comments are formatted to a depth of 2.
    Otherwise, we don't get the comments.
    """
    if isinstance(story, int):
        story = _get_story_info(story)
    output = {
        "id": story["story_id"],
        "author": story["author"],
    }
    if "title" in story:
        output["title"] = story["title"]
    if "points" in story:
        output["points"] = story["points"]
    if "url" in story:
        output["url"] = story["url"]
    if not basic:
        if _validate_comments_is_list_of_dicts(story["children"]):
            story = _get_story_info(story["story_id"])
        output["comments"] = [
            _format_comment_details(child) for child in story["children"]
        ]
    return output

def _format_comment_details(comment: Dict, depth: int = DEFAULT_COMMENT_DEPTH, num_comments: int = DEFAULT_NUM_COMMENTS) -> Dict:
    """
    Returns a dictionary with the following details:
    {
        "author": str,
        "text": str,
        "children": List[Dict] # in the same format as the parent
    }
    """
    output = {
        "author": comment["author"],
        "text": comment["text"],
    }
    if depth > 1 and len(comment["children"]) > 0:
        output["comments"] = [
            _format_comment_details(child, depth - 1, num_comments) for child in comment["children"][:num_comments]
        ]
    return output

def get_top_stories(num_stories: int = DEFAULT_NUM_STORIES):
    """
    Returns a list of dictionaries with the following details:
    {
        "id": int,
        "title": str,
        "url": str,
        "author": str,
        "points": int (nullable),
    }
    """
    url = f"{BASE_API_URL}/search?tags=front_page&hitsPerPage={num_stories}"
    response = requests.get(url)
    response.raise_for_status()
    return [_format_story_details(story) for story in response.json()["hits"]]

def get_new_stories(num_stories: int = DEFAULT_NUM_STORIES):
    """
    Returns a list of dictionaries with the following details:
    {
        "id": int,
        "title": str,
        "url": str,
        "author": str,
        "points": int (nullable),
    }
    """
    url = f"{BASE_API_URL}/search_by_date?tags=story&hitsPerPage={num_stories}"
    response = requests.get(url)
    response.raise_for_status()
    return [_format_story_details(story) for story in response.json()["hits"]]

def get_show_hn_stories(num_stories: int = DEFAULT_NUM_STORIES):
    """
    Returns a list of dictionaries with the following details:
    {
        "id": int,
        "title": str,
        "url": str,
        "author": str,
        "points": int (nullable),
    }
    """
    url = f"{BASE_API_URL}/search?tags=show_hn&hitsPerPage={num_stories}"
    response = requests.get(url)
    response.raise_for_status()
    return [_format_story_details(story) for story in response.json()["hits"]]

def get_ask_hn_stories(num_stories: int = DEFAULT_NUM_STORIES):
    """
    Returns a list of dictionaries with the following details:
    {
        "id": int,
        "title": str,
        "url": str,
        "author": str,
        "points": int (nullable),
    }
    """
    url = f"{BASE_API_URL}/search?tags=ask_hn&hitsPerPage={num_stories}"
    response = requests.get(url)
    response.raise_for_status()
    return [_format_story_details(story) for story in response.json()["hits"]]

def search_stories(query: str, num_results: int = DEFAULT_NUM_STORIES, search_by_date: bool = False):
    """
    Returns a list of dictionaries with the following details:
    {
        "id": int,
        "title": str,
        "url": str,
        "author": str,
        "points": int (nullable),
    }

    If search_by_date is True, then we search by date, otherwise, we use relevance, then points, then number of comments.
    """
    if search_by_date:
        url = f"{BASE_API_URL}/search_by_date?query={query}&hitsPerPage={num_results}&tags=story"
    else:
        url = f"{BASE_API_URL}/search?query={query}&hitsPerPage={num_results}&tags=story"
    print(url)
    response = requests.get(url)
    response.raise_for_status()
    return [_format_story_details(story) for story in response.json()["hits"]]

def get_story_info(story_id: int) -> Dict:
    """
    Returns a dictionary with the following details:
    {
        "id": int,
        "title": str,
        "url": str (nullable),
        "author": str,
        "points": int (nullable),
        "comments": List[Dict]
    }
    """
    story = _get_story_info(story_id)
    return _format_story_details(story, basic=False)

def _get_user_stories(user_name: str, num_stories: int = DEFAULT_NUM_STORIES) -> List[Dict]:
    url = f"{BASE_API_URL}/search?tags=author_{user_name},story&hitsPerPage={num_stories}"
    response = requests.get(url)
    response.raise_for_status()
    return [_format_story_details(story) for story in response.json()["hits"]]

def get_user_info(user_name: str, num_stories: int = DEFAULT_NUM_STORIES) -> Dict:
    url = f"{BASE_API_URL}/users/{user_name}"
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    response["stories"] = _get_user_stories(user_name, num_stories)
    return response
