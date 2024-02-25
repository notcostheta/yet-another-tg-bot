import asyncio
from telegraph.aio import Telegraph
from telegraph.exceptions import TelegraphException
from bot.configs.config import SESSION_NAME

telegraph_name = "pierated"


async def telegraph_paste(page_title: str, content: list) -> str:
    telegraph = Telegraph(domain="te.legra.ph")

    try:
        await telegraph.create_account(short_name=telegraph_name)
        response = await telegraph.create_page(
            title=page_title if len(page_title) < 256 else page_title[:253] + "...",
            author_name=telegraph_name,
            author_url="https://t.me/" + telegraph_name,
            content=content,
        )
        return "https://te.legra.ph/" + response["path"]
    except TelegraphException as e:
        # Create multiple pages if the content is too large
        content = [content[i : i + 3] for i in range(0, len(content), 3)]
        pages = []
        for i, page in enumerate(content):
            title = f"{page_title} - {i+1}"
            response = await telegraph.create_page(
                title=title if len(title) < 256 else title[:253] + "...",
                author_name=telegraph_name,
                author_url="https://t.me/" + telegraph_name,
                content=page,
            )
            pages.append("https://te.legra.ph/" + response["path"])
        return pages


## Defined get_telegraph_caption for further reference, won't be using it this time

# async def get_telegraph_caption(metadata: dict, album: list) -> list:
#     artist_id = metadata["artist"]["id"]
#     artist_url = f"https://open.spotify.com/artist/{artist_id}"
#     album_url = f"https://open.spotify.com/album/{album[0].album_id}"

#     content = [
#         {"tag": "img", "attrs": {"src": album[0].cover_url}},
#         # {"tag": "br"},
#         {"tag": "h3", "children": ["Metadata"]},
#         {"tag": "strong", "children": ["Album: "]},
#         {
#             "tag": "a",
#             "attrs": {"href": album_url, "target": "_blank", "rel": "noopener"},
#             "children": [album[0].album_name],
#         },
#         {"tag": "br"},
#         {"tag": "strong", "children": ["Artists: "]},
#         {
#             "tag": "a",
#             "attrs": {"href": artist_url, "target": "_blank", "rel": "noopener"},
#             "children": [album[0].album_artist],
#         },
#         {"tag": "br"},
#         {"tag": "strong", "children": ["Released On: "]},
#         {"tag": "p", "children": [album[0].date]},
#         {"tag": "br"},
#         {"tag": "strong", "children": ["Total Tracks: "]},
#         {"tag": "p", "children": [str(album[0].tracks_count)]},
#         {"tag": "br"},
#         {"tag": "h3", "children": ["Tracks"]},
#     ]

#     track_list = [{"tag": "ol", "children": []}]
#     for track in album:
#         track_list[0]["children"].append(
#             {
#                 "tag": "li",
#                 "children": [
#                     {
#                         "tag": "a",
#                         "attrs": {
#                             "href": track.url,
#                             "target": "_blank",
#                             "rel": "noopener",
#                         },
#                         "children": [track.name],
#                     }
#                 ],
#             }
#         )
#     content.extend(track_list)
#     return content
