# ライブラリ修正用
import os

from ebooklib.epub import NAMESPACES, EpubHtml, Section, Link
from ebooklib.utils import parse_string, parse_html_string
from lxml import etree


def my_get_nav(self, item):
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

    _body = etree.SubElement(tree_root, 'body')
    if self.direction:
        _body.set('dir', self.direction)

    body = html_tree.find('body')
    if body is not None:
        for i in body.getchildren():
            _body.append(i)

    tree_str = etree.tostring(tree, pretty_print=True, encoding='utf-8', xml_declaration=True)

    return tree_str