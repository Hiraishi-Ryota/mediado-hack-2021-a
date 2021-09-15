import collections
import re
import uuid
from io import BytesIO
from PIL import Image
from typing import Iterable, List

import ebooklib
from ebooklib import epub
from ebooklib.epub import EpubWriter, EpubHtml


from books import schemas
from ebook_split import ebooklib_patch


def flatten(iterable: Iterable):
    for elm in iterable:
        # 仕様上文字列やバイト列は現れないため，チェックは省略
        if isinstance(elm, collections.abc.Iterable):
            yield from flatten(elm)
        else:
            yield elm


# ライブラリの応急処置
EpubWriter._get_nav = ebooklib_patch.my_get_nav
EpubHtml.get_content = ebooklib_patch.my_get_content


class EpubSplitter:
    def __init__(self, path: str) -> None:
        self.path = path
        self.epub_data = epub.read_epub(path)
        self.identifier = self.epub_data.get_metadata("DC", "identifier")[0][0]
        self.title = self.epub_data.get_metadata("DC", "title")[0][0]
        self.language = self.epub_data.get_metadata("DC", "language")[0][0]

        try:
            self.cover_image = list(self.epub_data.get_items_of_type(ebooklib.ITEM_COVER))[0]
        except KeyError:
            self.cover_image = None

        try:
            self.creator = list(self.epub_data.get_metadata("DC", "creator"))[0][0]
        except KeyError:
            self.creator = None

        # epub内に含まれるファイル情報を取得
        self.html_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        self.css_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_STYLE))

        self.css_files = [self._reconstruct_epub_item(css) for css in self.css_files]

        self.img_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_IMAGE))
        self.font_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_FONT))
        self.audio_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_AUDIO))
        self.video_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_VIDEO))
        self.js_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_SCRIPT))
        self.vector_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_VECTOR))
        self.unknown_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_UNKNOWN))

        self.nav_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_NAVIGATION))

    def _procese_toc(self) -> List:
        """ Get a chapter of list from the toc of the book """
        toc = self.epub_data.toc

        print(toc)

        regex_backslash = re.compile(r"\\[^\s]+")
        regex_white_space = re.compile(r"\s+")

        chapter_list = []
        for chapter in toc:
            html_list = []
            if isinstance(chapter, epub.Link):
                html = chapter.href.split("#")[0]
                title = chapter.title

                title = regex_backslash.sub("", title)
                title = regex_white_space.sub("", title)

                chapter_info = {"title": title, "html_list": html_list}
                chapter_list.append(chapter_info)
                html_list.append(html)
            else:
                # TODO Sectionが存在する場合に対応する．
                # title = chapter[0].title
                #
                # title = regex_backslash.sub("", title)
                # title = regex_white_space.sub("", title)

                title = None
                flatten_chapter = flatten(chapter)

                for elm in flatten_chapter:
                    html = elm.href.split("#")[0]
                    if html not in html_list:
                        html_list.append(html)

                chapter_info = {"title": title, "html_list": html_list}
                chapter_list.append(chapter_info)

        # flatten_toc = flatten(toc)
        # print(list(flatten_toc))

        # html_list = []
        # chapter_list = []
        # title = None
        # for chapter in flatten_toc:
        #     html = chapter.href.split("#")[0]
        #
        #     # 子要素（さらに小さい章）がある
        #     if isinstance(chapter, epub.Section):
        #         # TODO if文のネスト無くせないか？
        #         if not html_list:
        #             chapter_info = {"title": title, "html_list": html_list}
        #             chapter_list.append(chapter_info)
        #             html_list.clear()
        #
        #         title = chapter.title
        #
        #     if html not in html_list:
        #         html_list.append(html)
        # else:
        #     # TODO 共通化したい
        #     chapter_info = {"title": title, "html_list": html_list}
        #     chapter_list.append(chapter_info)

        return chapter_list

    def _reconstruct_epub_item(self, item: epub.EpubItem):
        """ Reconstruct epub_item to adopt the form of ebooklib """
        return epub.EpubItem(uid=item.get_id(), file_name="css/" + item.get_name().split("/")[-1],
                             content=item.get_content(), media_type="text/css", manifest=True)

    def create_chapters(self, path: str, price: int):
        """ create_chapters calls _create_chapter and return the book's information """

        chapter_list = self._procese_toc()

        # ランダムなファイル名生成
        cover_image_name = self.cover_image.get_name().split("/")[-1]
        cover_image_name = self._get_random_name(cover_image_name, 20)

        # カバー画像を保存
        cover_image = Image.open(BytesIO(self.cover_image.get_content()))

        cover_image.save("static/book_cover_img/" + cover_image_name)

        chapter_create_list = []

        # idは章番号を求めるために用いる
        for id, chapter in enumerate(chapter_list):
            epub_path = self._create_chapter(id + 1, chapter["html_list"])

            chapter = schemas.ChapterCreate(
                title=chapter["title"] != "" if chapter["title"] else "Chapter {}".format(id+1),
                price=0,
                author=self.creator,
                e_pub=epub_path,
                word_count=0,
                chapter_num=id+1
            )
            chapter_create_list.append(chapter)

        ebook_data = schemas.BookCreateConfirm(
            title=self.title,
            price=price,
            author=self.creator,
            cover_img="static/book_cover_img/" + cover_image_name,
            word_count=0,
            e_pub=path,
            chapters=chapter_create_list
        )

        return ebook_data

    def _create_chapter(self, id: int, html_list: List[str]):
        """ Create chapter from given html_list and css_files """

        book = epub.EpubBook()

        # メタデータの設定
        # TODO より多くのメタデータに対応(publisher, contributorなど)
        book.set_identifier("{}-{}".format(self.identifier, id))
        book.set_title(self.title)
        book.set_language(self.language)
        if self.creator is not None:
            book.add_author(self.creator)

        book.add_item(self.cover_image)

        spine = []

        # CSSファイルを追加
        for css in self.css_files:
            book.add_item(css)

        # 画像ファイル追加
        for img in self.img_files:
            book.add_item(img)

        # フォントファイル追加
        for font in self.font_files:
            book.add_item(font)

        # オーディオファイルの追加
        for audio in self.audio_files:
            book.add_item(audio)

        # 動画ファイルを追加
        for video in self.video_files:
            book.add_item(video)

        # scriptファイルの追加
        for js in self.js_files:
            book.add_item(js)

        # vectorファイルの追加
        for vector in self.vector_files:
            book.add_item(vector)

        # そのほかのファイルの追加
        for unknown in self.unknown_files:
            book.add_item(unknown)

        # HTMLファイルを検索し，本に追加
        for html in html_list:
            h = self._find_html(html, self.html_files)

            for css in self.css_files:
                h.add_item(css)

            book.add_item(h)
            spine.append(h)

        # 目次の作成 TODO 目次をインスタンス変数化
        # book.toc = self.epub_data.toc

        # 目次のxhtmlファイル
        nav = epub.EpubNav()

        # 目次にもcssファイルを追加
        for css in self.css_files:
            nav.add_item(css)

        # TODO 目次の実装
        # book.toc = (self.epub_data.toc[id-1],)
        book.spine = [nav] + spine

        book.add_item(epub.EpubNcx())
        book.add_item(nav)

        filename = f"static/bibi-bookshelf/{uuid.uuid4()}.epub"
        try:
            epub.write_epub(filename, book)
        except:
            filename = ""
        return filename

    def _find_html(self, target_html: str, html_files):
        """ Find target_html from html_files """
        for html_file in html_files:
            if target_html == html_file.get_name():
                return html_file

    def _get_random_name(self, original_file_name: str, n: int):
        """ Add random n characters to file_name """
        file_split = original_file_name.split(".")

        # name = [random.choice(string.ascii_letters + string.digits) for _ in range(n)]
        #
        # file_split[-2] += "".join(name)
        file_split[-2] += ("-" + f"{uuid.uuid4()}")
        return ".".join(file_split)


def parse_ebook(path: str, price: int):
    # 本を分割する部分
    book = EpubSplitter(path)

    ebook_data = book.create_chapters(path, price)

    return ebook_data


def get_text_by_path(path: str):
    book = epub.read_epub(path)
    documents = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)

    text_list = [str(document.get_body_content()) for document in documents]
    text = " ".join(text_list)

    # タグなど，不要な情報を削除
    regex_video_tag = re.compile(r"<video[^>]*>.*</video>")
    regex_tag = re.compile(r"<[^>]*?>")
    regex_backslash = re.compile(r"\\[^\s]+")
    regex_white_space = re.compile(r"\s+")

    s = regex_video_tag.sub("", text)
    s = regex_tag.sub("", s)
    s = regex_backslash.sub("", s)
    s = regex_white_space.sub(" ", s)

    return s


if __name__ == "__main__":
    ebook_data = parse_ebook("/Users/h4d9x/mediado-hack-2021-a/src/backend/static/bookshelf/accessible_epub_3.epub", 1000)
    print(ebook_data)
    # print(get_text_by_path("/Users/h4d9x/mediado-hack-2021-a/src/backend/static/bookshelf/5efe071c-65ef-4fb8-bc4d-c3ab156453b7.epub"))
