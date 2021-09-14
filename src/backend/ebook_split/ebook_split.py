import os
import uuid
from io import BytesIO
from PIL import Image
from typing import Iterable, List

import ebooklib
from ebooklib import epub
from ebooklib.epub import EpubWriter, NAMESPACES, EpubHtml, Section, Link

from ebooklib.utils import parse_string, parse_html_string
from lxml import etree

from src.backend.books import schemas


# def flatten(iterable: Iterable):
#     for elm in iterable:
#         # 仕様上文字列やバイト列は現れないため，チェックは省略
#         if isinstance(elm, collections.abc.Iterable):
#             yield from flatten(elm)
#         else:
#             yield elm


# ライブラリ修正用
def _my_get_nav(self, item):
    # just a basic navigation for now
    nav_xml = parse_string(self.book.get_template('nav'))
    root = nav_xml.getroot()

    root.set('lang', self.book.language)
    root.attrib['{%s}lang' % NAMESPACES['XML']] = self.book.language

    nav_dir_name = os.path.dirname(item.file_name)

    head = etree.SubElement(root, 'head')
    title = etree.SubElement(head, 'title')
    title.text = self.book.title

    # for now this just handles css files and ignores others
    for _link in item.links:
        _lnk = etree.SubElement(head, 'link', {
            'href': _link.get('href', ''), 'rel': 'stylesheet', 'type': 'text/css'
        })

    body = etree.SubElement(root, 'body')
    nav = etree.SubElement(body, 'nav', {
        '{%s}type' % NAMESPACES['EPUB']: 'toc',
        'id': 'id',
        'role': 'doc-toc',
    })

    content_title = etree.SubElement(nav, 'h2')
    content_title.text = self.book.title

    def _create_section(itm, items):
        ol = etree.SubElement(itm, 'ol')
        for item in items:
            if isinstance(item, tuple) or isinstance(item, list):
                li = etree.SubElement(ol, 'li')
                if isinstance(item[0], EpubHtml):
                    a = etree.SubElement(li, 'a', {'href': os.path.relpath(item[0].file_name, nav_dir_name)})
                elif isinstance(item[0], Section) and item[0].href != '':
                    a = etree.SubElement(li, 'a', {'href': os.path.relpath(item[0].href, nav_dir_name)})
                elif isinstance(item[0], Link):
                    a = etree.SubElement(li, 'a', {'href': os.path.relpath(item[0].href, nav_dir_name)})
                else:
                    a = etree.SubElement(li, 'span')
                a.text = item[0].title

                _create_section(li, item[1])

            elif isinstance(item, Link):
                li = etree.SubElement(ol, 'li')
                a = etree.SubElement(li, 'a', {'href': os.path.relpath(item.href, nav_dir_name)})
                a.text = item.title
            elif isinstance(item, EpubHtml):
                li = etree.SubElement(ol, 'li')
                a = etree.SubElement(li, 'a', {'href': os.path.relpath(item.file_name, nav_dir_name)})
                a.text = item.title

    _create_section(nav, self.book.toc)

    # LANDMARKS / GUIDE
    # - http://www.idpf.org/epub/30/spec/epub30-contentdocs.html#sec-xhtml-nav-def-types-landmarks

    if len(self.book.guide) > 0 and self.options.get('epub3_landmark'):

        # Epub2 guide types do not map completely to epub3 landmark types.
        guide_to_landscape_map = {
            'notes': 'rearnotes',
            'text': 'bodymatter'
        }

        guide_nav = etree.SubElement(body, 'nav', {'{%s}type' % NAMESPACES['EPUB']: 'landmarks'})

        guide_content_title = etree.SubElement(guide_nav, 'h2')
        guide_content_title.text = self.options.get('landmark_title', 'Guide')

        guild_ol = etree.SubElement(guide_nav, 'ol')

        for elem in self.book.guide:
            li_item = etree.SubElement(guild_ol, 'li')

            if 'item' in elem:
                chap = elem.get('item', None)
                if chap:
                    _href = chap.file_name
                    _title = chap.title
            else:
                _href = elem.get('href', '')
                _title = elem.get('title', '')

            guide_type = elem.get('type', '')
            a_item = etree.SubElement(li_item, 'a', {
                '{%s}type' % NAMESPACES['EPUB']: guide_to_landscape_map.get(guide_type, guide_type),
                'href': os.path.relpath(_href, nav_dir_name)
            })
            a_item.text = _title

    tree_str = etree.tostring(nav_xml, pretty_print=True, encoding='utf-8', xml_declaration=True)

    return tree_str


# ライブラリ修正用
def my_get_content(self, default=None):
    """
    Returns content for this document as HTML string. Content will be of type 'str' (Python 2)
    or 'bytes' (Python 3).

    :Args:
      - default: Default value for the content if it is not defined.

    :Returns:
      Returns content of this document.
    """

    tree = parse_string(self.book.get_template(self._template_name))
    tree_root = tree.getroot()

    tree_root.set('lang', self.lang or self.book.language)
    tree_root.attrib['{%s}lang' % NAMESPACES['XML']] = self.lang or self.book.language

    # add to the head also
    #  <meta charset="utf-8" />

    try:
        html_tree = parse_html_string(self.content)
    except:
        return ''

    html_root = html_tree.getroottree()

    # create and populate head

    _head = etree.SubElement(tree_root, 'head')

    if self.title != '':
        _title = etree.SubElement(_head, 'title')
        _title.text = self.title

    for lnk in self.links:
        lnk["href"] = "../" + lnk["href"]
        if lnk.get('type') == 'text/javascript':
            _lnk = etree.SubElement(_head, 'script', lnk)
            # force <script></script>
            _lnk.text = ''
        else:
            _lnk = etree.SubElement(_head, 'link', lnk)

    # this should not be like this
    # head = html_root.find('head')
    # if head is not None:
    #     for i in head.getchildren():
    #         if i.tag == 'title' and self.title != '':
    #             continue
    #         _head.append(i)

    # create and populate body

    _body = etree.SubElement(tree_root, 'body')
    if self.direction:
        _body.set('dir', self.direction)

    body = html_tree.find('body')
    if body is not None:
        for i in body.getchildren():
            _body.append(i)

    tree_str = etree.tostring(tree, pretty_print=True, encoding='utf-8', xml_declaration=True)

    return tree_str


EpubWriter._get_nav = _my_get_nav
EpubHtml.get_content = my_get_content


class EpubSplit:
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

        print(self.cover_image)

        try:
            self.creator = list(self.epub_data.get_metadata("DC", "creator"))[0][0]
        except KeyError:
            self.creator = None

    def split_book(self):
        html_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        css_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_STYLE))

        css_files = [self._reconstruct_epub_item(css) for css in css_files]

        chapter_list = self._procese_toc()
        print(chapter_list)

        # idは章番号を求めるために用いる
        for id, chapter in enumerate(chapter_list):
            self._create_book(id + 1, chapter["html_list"], html_files, css_files)

    # Get a chapter of list from the toc of the book
    def _procese_toc(self) -> List:
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

    def _reconstruct_epub_item(self, item: epub.EpubItem):
        return epub.EpubItem(uid=item.get_id(), file_name="css/" + item.get_name().split("/")[-1],
                             content=item.get_content(), media_type="text/css", manifest=True)

    def create_chapters(self, path: str, price: int):
        html_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        css_files = list(self.epub_data.get_items_of_type(ebooklib.ITEM_STYLE))

        css_files = [self._reconstruct_epub_item(css) for css in css_files]

        chapter_list = self._procese_toc()

        cover_image_name = self.cover_image.get_name().split("/")[-1]

        # カバー画像を保存
        cover_image = Image.open(BytesIO(self.cover_image.get_content()))
        cover_image.save("static/book_cover_img/" + cover_image_name)

        chapter_create_list = []

        # idは章番号を求めるために用いる
        for id, chapter in enumerate(chapter_list):
            epub_path = self._create_book(id + 1, chapter["html_list"], html_files, css_files)

            chapter = schemas.ChapterCreate(
                title=self.title,
                price=price,
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
            cover_img=cover_image_name,
            word_count=0,
            e_pub=path,
            chapters=chapter_create_list
        )

        return ebook_data

    # Create book from given arguments and instance variables
    def _create_book(self, id: int, html_list: List[str], html_files: List, css_files: List):
        book = epub.EpubBook()

        # メタデータの設定
        # TODO より多くのメタデータに対応(atuhor, publisher, contributorなど)
        book.set_identifier("{}-{}".format(self.identifier, id))
        book.set_title(self.title)
        book.set_language(self.language)
        if self.creator is not None:
            book.add_author(self.creator)

        # TODO カバー画像の追加
        book.add_item(self.cover_image)

        spine = []

        # CSSファイルを追加
        for css in css_files:
            book.add_item(css)

        # HTMLファイルを検索し，本に追加
        for html in html_list:
            h = self._find_html(html, html_files)

            # TODO CSS
            for css in css_files:
                h.add_item(css)

            book.add_item(h)
            spine.append(h)

        # 目次の作成 TODO 目次をインスタンス変数化
        print(self.epub_data.toc[id - 1])

        # TODO 目次の実装
        # book.toc = (self.epub_data.toc[id-1],)
        book.spine = ["nav"] + spine

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # TODO 生成場所の調整
        filename = f"static/bookshelf/{uuid.uuid4()}.epub"
        try:
            epub.write_epub(filename, book)
        except:
            filename = ""
        return filename

    # Find target_html from html_files
    def _find_html(self, target_html: str, html_files):
        for html_file in html_files:
            if target_html == html_file.get_name():
                return html_file

    # return item’s name (usually filename) of the file
    def _get_item_names(self, items):
        item_names = [item.get_name for item in items]


def parse_ebook(path: str, price: int):
    # 本を分割する部分
    book = EpubSplit(path)

    ebook_data = book.create_chapters(path, price)

    return ebook_data


if __name__ == "__main__":
    ebook_data = parse_ebook("/Users/h4d9x/Documents/バックエンド/Python/epub/cc-shared-culture.epub", 1000)
    print(ebook_data)
