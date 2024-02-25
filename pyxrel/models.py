from typing import List, Optional, Union

from pydantic import BaseModel, HttpUrl


class Category(BaseModel):
    name: str
    parent_cat: Optional[str]


class CategoryP2P(BaseModel):
    meta_cat: str
    sub_cat: Optional[str]
    id: str


class Categories(BaseModel):
    list: List[Category]


class CategoriesP2P(BaseModel):
    list: List[CategoryP2P]


class Pagination(BaseModel):
    current_page: int
    per_page: int
    total_pages: int


class ReleaseSize(BaseModel):
    number: int
    unit: str


class ExternalSource(BaseModel):
    id: int
    name: str


class Externals(BaseModel):
    source: ExternalSource
    link_url: HttpUrl
    plot: Optional[str] = None


class ReleaseDates(BaseModel):
    type: str
    date: str


class Media(BaseModel):
    type: str
    description: Optional[str] = None
    time: int
    url_full: Optional[HttpUrl] = None
    url_thumb: Optional[HttpUrl] = None
    video_url: Optional[HttpUrl] = None
    youtube_id: Optional[str] = None


class MediaList(BaseModel):
    list: List[Media]


class ReleaseFlags(BaseModel):
    english: bool = False
    fix_rls: bool = False
    nuke_rls: bool = False
    top_rls: bool = False


class ReleaseExtInfo(BaseModel):
    type: str
    id: str
    title: str
    link_href: HttpUrl
    rating: float = None
    num_ratings: Optional[int] = None
    uris: List[str] = []


class GroupP2P(BaseModel):
    id: str
    name: str


class ReleaseP2P(BaseModel):
    id: str
    dirname: str
    link_href: HttpUrl
    category: Optional[CategoryP2P] = None
    main_lang: str
    pub_time: int
    post_time: Optional[int] = None
    size_mb: int
    group: Optional[GroupP2P] = None
    num_ratings: int
    ext_info: ReleaseExtInfo
    comments: int


class Release(BaseModel):
    id: str
    dirname: str
    link_href: HttpUrl
    time: int
    group_name: str
    size: ReleaseSize
    video_type: str
    audio_type: str
    num_ratings: int
    tv_season: Optional[int] = None
    tv_episode: Optional[int] = None
    video_rating: Optional[float] = None
    audio_rating: Optional[float] = None
    ext_info: ReleaseExtInfo
    comments: int
    proof_url: str = None
    flags: ReleaseFlags


class FiltersItem(BaseModel):
    id: int
    name: str


class AddProof(BaseModel):
    proof_url: HttpUrl
    releases: List[str]


class ExtInfoInfo(BaseModel):
    type: str
    id: str
    title: str
    link_href: HttpUrl
    genre: str
    alt_title: Optional[str] = None
    cover_url: HttpUrl
    uris: List[str]
    rating: float
    num_ratings: int
    release_dates: Optional[List[ReleaseDates]] = []
    externals: List[Externals]


class SearchResult(BaseModel):
    total: int
    results: List[Release] = []
    p2p_results: List[ReleaseP2P]


class ResultsExtInfo(BaseModel):
    total: int
    result: ExtInfoInfo


class Releases(BaseModel):
    total_count: int
    pagination: Pagination
    list: List[Release]


class ReleasesP2P(BaseModel):
    total_count: int
    pagination: Pagination
    list: List[ReleaseP2P]


class Filters(BaseModel):
    filters: List[FiltersItem]


class CommentAuthor(BaseModel):
    id: str
    name: str


class TextAttachment(BaseModel):
    id: str
    mime_type: str
    image_width: int
    image_height: int
    image_width_thumb: int
    image_height_thumb: int
    image_full: HttpUrl
    image_thumb: HttpUrl


class CommentRating(BaseModel):
    video: int = None
    audio: int = None


class CommentVote(BaseModel):
    positive: int = None
    negative: int = None


class CommentEdits(BaseModel):
    count: int = None
    last: int = None


class Comment(BaseModel):
    id: str
    time: int
    author: CommentAuthor
    link_href: str
    text: str
    text_preview_html: Union[str, None]
    text_attachments: Union[List[TextAttachment], None]
    rating: CommentRating
    votes: CommentVote
    edits: CommentEdits


class Comments(BaseModel):
    total_count: int
    pagination: Pagination = None
    list: List[Comment]


class MinRelease(BaseModel):
    id: str
    dirname: str
    link_href: HttpUrl
    time: int
    flags: ReleaseFlags


class MinReleaseP2P(BaseModel):
    id: str
    dirname: str
    link_href: HttpUrl
    pub_time: int


class ExtInfoItem(BaseModel):
    type: str
    id: str
    title: str
    link_href: str
    genre: str = None
    alt_title: Optional[str] = None
    cover_url: str = None
    releases: Optional[List[MinRelease]] = []
    p2p_releases: Optional[List[MinReleaseP2P]] = []


class Upcoming(BaseModel):
    list: List[ExtInfoItem]


class SearchExtInfo(BaseModel):
    total: int
    results: List[ExtInfoItem] = []
