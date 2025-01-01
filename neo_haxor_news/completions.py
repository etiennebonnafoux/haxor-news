from neo_haxor_news.settings import freelancer_post_id, who_is_hiring_post_id
from dataclasses import dataclass


@dataclass
class OptsLookup:
    args: str
    opts: list[str]


FREELANCER_POST_ID = str(freelancer_post_id)
WHO_IS_HIRING_POST_ID = str(who_is_hiring_post_id)
SUBCOMMANDS: dict[str, str] = {
    "ask": "Ask HN posts",
    "best": "Best of HN weekly posts",
    "freelance": "Monthly freelancers post",
    "hiring": "Monthly hiring post",
    "jobs": "Jobs posts",
    "new": "Newest posts",
    "show": "Show HN posts",
    "top": "Top posts",
    "user": "User info",
    "view": "View specified post",
}
ARGS_OPTS_LOOKUP: dict[str, OptsLookup] = {
    "freelance": OptsLookup(
        '"(?i)(Python|Django)"',
        [
            "--id_post " + FREELANCER_POST_ID,
            "-i " + FREELANCER_POST_ID,
        ],
    ),
    "hiring": OptsLookup(
        '"(?i)(Python|Django)"',
        [
            "--id_post " + WHO_IS_HIRING_POST_ID,
            "-i " + WHO_IS_HIRING_POST_ID,
        ],
    ),
    "user": OptsLookup(
        '"user"',
        [
            "--limit 10",
            "-l 10",
        ],
    ),
    "view": OptsLookup(
        "1",
        [
            '--comments_regex_query ""',
            '-cq ""',
            "--comments",
            "-c",
            "--comments_recent",
            "-cr",
            "--comments_unseen",
            "-cu",
            "--comments_hide_non_matching",
            "-ch",
            "--clear_cache",
            "-cc",
            "--browser",
            "-b",
        ],
    ),
}
META_LOOKUP: dict[str, str] = {
    "10": "limit: int (opt) limits the posts displayed",
    '"(?i)(Python|Django)"': (
        "regex_query: string (opt) applies a regular " "expression comment filter"
    ),
    "1": "index: int (req) views the post index",
    '"user"': "user:string (req) shows info on the specified user",
    '--comments_regex_query ""': (
        "Filter comments with a regular expression" " query (string)"
    ),
    '-cq ""': ("Filter comments with a regular expression" " query (string)"),
    "--comments": "View comments instead of the url contents (flag)",
    "-c": "View comments instead of the url contents (flag)",
    "--comments_recent": "View only comments in the past hour (flag)",
    "-cr": "View only comments in the past hour (flag)",
    "--comments_unseen": "View only previously unseen comments (flag)",
    "-cu": "View only previously unseen comments (flag)",
    "--comments_hide_non_matching": (
        "Hide instead of collapse " "non-matching comments (flag)"
    ),
    "-ch": "Hide instead of collapse non-matching comments (flag)",
    "--clear_cache": "Clear the comment cache before executing.",
    "-cc": "Clear the comment cache before executing.",
    "--browser": "View in a browser instead of the terminal (flag)",
    "-b": "View in a browser instead of the terminal (flag)",
    "--id_post " + WHO_IS_HIRING_POST_ID: (
        "View matching comments from "
        "the (optional) post id instead"
        " of the latest post (int)"
    ),
    "-i " + WHO_IS_HIRING_POST_ID: (
        "View matching comments from "
        "the (optional) post id instead"
        " of the latest post (int)"
    ),
    "--limit 10": "Limits the number of user submissions displayed (int)",
    "-l 10": "Limits the number of user submissions displayed (int)",
}
META_LOOKUP.update(SUBCOMMANDS)
