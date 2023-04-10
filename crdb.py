#! /usr/bin/python3
# -*- coding: utf-8 -*-

# from xml.dom import minidom as XMLDOM
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import datetime
# import html
import logging
import os
import shutil
import uuid


logger = logging.getLogger(__name__)


class ComicDB(object):
    """ A ComicRack database... """

    ElementTree.register_namespace("xsd", "http://www.w3.org/2001/XMLSchema")
    ElementTree.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")

    def __init__(self, filepath):
        if not os.path.isfile(filepath):
            raise ValueError("must be a valid file.")
        self._filepath = filepath
        self._loaded = False
        self._tree = None
        self._root = None

    def Load(self, forced=False):
        logger.info(f"called Load(forced={forced})")
        if not self._loaded or forced:
            logger.debug(f"calling ET.parse({self._filepath})")
            self._tree = ElementTree.parse(self._filepath)
            self._root = self._tree.getroot()
            self._loaded = True
            logger.info("loaded.")

    def Import(self, fp, forced=False):
        """creates a book from xml at fp"""
        logger.info(f"called Import(fp={fp},forced={forced}")
        if self._loaded:
            n_t = ElementTree.parse(fp)
            e_n = n_t.getroot()
            e_id = e_n.get("Id")
            logger.debug(f"import id = {e_id}")
            preexisting_books = self._root.findall(f"./Books/Book[@Id='{e_id}']")
            l_pre_n = len(preexisting_books)
            logger.debug(f"l_pre_n = {l_pre_n}")
            if l_pre_n == 0:
                all_books = self._root.find("./Books")
                all_books.append(e_n)
            elif l_pre_n > 0 and forced:
                all_books = self._root.find("./Books")
                for book in preexisting_books:
                    all_books.remove(book)
                all_books.append(e_n)
            else:
                raise ValueError(f"{e_id} already exists")
            logger.info("imported.")

    def Save(self):
        if self._loaded:
            logger.debug(f"writing xml to {self._filepath}")
            self._tree.write(self._filepath, xml_declaration=True)
            logger.info("saved.")

    def Export(self, id, fp):
        """writes a file at fp in xml format containing book[id]"""
        if not self._loaded:
            self.Load()
        e_book = self._root.findall(f"./Books/Book[@Id='{id}']")[0]
        filepath = os.path.join(fp, f"{id}.xml")
        logger.debug(f"exporting {id} to {filepath}")
        book_t = ElementTree.ElementTree(e_book)
        book_t.write(filepath, encoding="utf-8", xml_declaration=True)
        logger.info("exported.")

    @property
    def Library(self):
        if not self._loaded:
            self.Load()
        logger.info("making a library...")
        bk_n = 0
        books = {}
        for b in self._root.findall("./Books/Book"):
            bk_n += 1
            books[b.get("Id")] = Book(b)
        logger.debug(f"bound {bk_n} books.")
        return Library(self, books)

    @Library.setter
    def Library(self, library):
        logger.info("replacing the library's books...")
        l = self._root.find("./Books")
        self._root.remove(l)
        self._root.append(library.XML)


class Library(dict):
    """A ComicRack Library."""

    def __init__(self, db, books):
        self._db = db
        self.__dict__ = books

    def Import(self, fp, forced=False):
        logger.info(f"called Import({fp},{forced})")
        with os.scandir(fp) as fp_d:
            for f in fp_d:
                f_ext = os.path.splitext(f)[1]
                if f_ext == '.xml':
                    self._db.Import(f, forced)

    def Export(self, fp):
        logger.info(f"called Export({fp})")
        for k in list(self.__dict__):
            self._db.Export(self.__dict__[k].get("Id"), fp)

    @property
    def XML(self):
        xml = Element("Books")
        for k in list(self.__dict__):
            xml.append(self.__dict__[k].XML)
        return xml


class Book(dict):
    """ A Comic Book. (V.ComicRack-Final) """

    def __init__(self, xml=None):
        self._xml = xml
        self._parse_xml()

    def _parse_xml(self):
        """xml to object."""
        xml = self._xml
        if xml is not None:
            i = xml.get("Id")
            f = xml.get("File")
            logger.debug(f"building obj for {i}")
            self.__dict__["Id"] = i
            self.__dict__["File"] = f
            for e in xml:
                self.__dict__[e.tag] = e.text

    def _render_xml(self):
        """object to xml."""
        xml = Element("Book")
        for k in list(self.__dict__):
            v = self.__dict__[k]
            if k in ["Id", "File"]:
                logger.debug(f"building xml for {v}")
                xml.set(k, v)
            else:
                e = Element(k)
                e.text = v
                xml.append(e)
        self._xml = xml

    def _bind(self, filepath):
        """binds an empty Book to a file. does NOT verify the path."""
        if self._xml is None:
            self.__dict__["Id"] = uuid.uuid4()
            self.__dict__["File"] = filepath
            self._render_xml()

    @property
    def XML(self):
        self._render_xml()
        return self._xml
