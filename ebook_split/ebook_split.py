import collections.abc
from typing import Iterable, List

import ebooklib
from ebooklib import epub


# def flatten(iterable: Iterable):
#     for elm in iterable:
#         # 仕様上文字列やバイト列は現れないため，チェックは省略
#         if isinstance(elm, collections.abc.Iterable):
#             yield from flatten(elm)
#         else:
#             yield elm


class EpubSplit:
    def __init__(self, path: str) -> None:
        self.path = path
        self.epub_data = epub.read_epub(path)
        self.identifier = self.epub_data.get_metadata("DC", "identifier")[0][0]
        self.title = self.epub_data.get_metadata("DC", "title")[0][0]
        self.language = self.epub_data.get_metadata("DC", "language")[0][0]

    def split_book(self):
        html_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        css_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_STYLE))

        chapter_list = self._procede_toc()
        print(chapter_list)

        # idは章番号を求めるために用いる
        for id, chapter in enumerate(chapter_list):
            self._create_book(id + 1, chapter["html_list"], html_files, css_files)

    # Get a chapter of list from the toc of the book
    def _procede_toc(self) -> List:
        toc = self.epub_data.toc

        chapter_list = []
        for chapter in toc:
            html_list = []
            html = chapter.href.split("#")[0]
            if isinstance(chapter, epub.Link):
                title = chapter.title
                chapter_info = {"title": title, "html_list": html_list}
                chapter_list.append(chapter_info)
                html_list.append(html)
            else:
                # TODO Sectionが存在する場合に対応する．
                pass

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

    # Create book from given arguments and instance variables
    def _create_book(self, id: int, html_list: List[str], html_files: List, css_files: List):
        book = epub.EpubBook()

        # メタデータの設定
        # TODO より多くのメタデータに対応(atuhor, publisher, contributorなど)
        book.set_identifier("{}-{}".format(self.identifier, id))
        book.set_title(self.title)
        book.set_language(self.language)

        # TODO カバー画像の追加

        # TODO 削除
        # html_files = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
        # css_files = book.get_items_of_type(ebooklib.ITEM_STYLE)

        spine = []
        # HTMLファイルを検索し，本に追加
        for html in html_list:
            h = self._find_html(html, html_files)

            # cssを追加する必要はあるのか？ TODO CSS
            for css in css_files:
                h.add_item(css)

            book.add_item(h)

            spine.append(h)

        # CSSファイルを追加
        # for css in css_files:
        #     css.set_name("Styles/" + css.get_name().split("/")[-1])
        #     book.add_item(css)

        # 目次の作成 TODO 目次をインスタンス変数化
        print(self.epub_data.toc[id-1])

        # TODO 目次の実装
        # book.toc = (self.epub_data.toc[id-1],)
        book.spine = ["nav"] + spine

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # TODO 生成場所の調整
        epub.write_epub("{}.epub".format(id), book)

    # Find target_html from html_files
    def _find_html(self, target_html: str, html_files):
        for html_file in html_files:
            if target_html == html_file.get_name():
                return html_file

    # return item’s name (usually filename) of the file
    def _get_item_names(self, items):
        item_names = [item.get_name for item in items]


if __name__ == "__main__":
    book = EpubSplit("cc-shared-culture.epub")
    book.split_book()
