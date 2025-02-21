import typing as t
from dataclasses import dataclass, field

from aiogram.enums import ContentType
from aiogram.types import InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo

from aiogram_mediagroup_handle._types import PhotoSize, Audio, Document, Video

MediaGroupType = list[InputMediaAudio | InputMediaDocument | InputMediaPhoto | InputMediaVideo]
MediaType = list[PhotoSize] | Audio | Document | Video

_media_mapping = {
    PhotoSize: InputMediaPhoto,
    Audio: InputMediaAudio,
    Document: InputMediaDocument,
    Video: InputMediaVideo,
}


def _unpack_type(obj):
    if isinstance(obj, list):
        return _unpack_type(obj[0])
    return type(obj)


@dataclass(slots=True, kw_only=True, frozen=True)
class MediaGroup:
    """Light weighted media group"""
    caption: t.Optional[str]
    photos: list[list[PhotoSize]] = field(default_factory=list)
    audio: list[Audio] = field(default_factory=list)
    documents: list[Document] = field(default_factory=list)
    video: list[Video] = field(default_factory=list)

    @property
    def content_type(self) -> str:
        """Return media group content type"""
        if self.photos:
            return ContentType.PHOTO
        if self.documents:
            return ContentType.DOCUMENT
        if self.audio:
            return ContentType.AUDIO
        if self.video:
            return ContentType.VIDEO

        return ContentType.UNKNOWN

    def __len__(self) -> int:
        return len(self.photos) + len(self.audio) + len(self.documents) + len(self.video)
