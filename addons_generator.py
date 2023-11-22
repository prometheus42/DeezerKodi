#!/usr/bin/python3

# *
# *  Copyright (C) 2012-2013 Garrett Brown
# *  Copyright (C) 2010      j48antialias
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# *  Based on code by j48antialias:
# *  https://anarchintosh-projects.googlecode.com/files/addons_xml_generator.py

""" addons.xml generator """

import os
import re
import shutil
import hashlib
from zipfile import ZipFile


def is_file_excluded(f):
    return f.endswith('.pyc') or f.endswith('.pyo')


def walk_dir(dir='.'):
    for root, dirs, files in os.walk(dir):
        for f in files:
            if not is_file_excluded(f):
                yield (f, '%s/%s' % (root, f))


class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
    """

    def generate_addons_file(self):
        # addon list
        addons = os.listdir(".")
        # skip artwork directory
        addons.remove('artwork')
        # final addons text
        addons_xml = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n"
        # loop thru and add each addons addon.xml file
        # compile addon version regex
        pattern = re.compile("version=[\"|\']([0-9\.]+)[\"|\']")
        for addon in addons:
            try:
                # skip any file or .svn folder or .git folder
                if (not os.path.isdir(addon) or addon == ".svn" or addon == ".git" or addon == ".idea"):
                    continue
                # create path
                _path = os.path.join(addon, "addon.xml")
                # split lines for stripping
                xml_lines = open(_path, "r").read().splitlines()
                # new addon
                addon_xml = ""
                # loop thru cleaning each line
                for line in xml_lines:
                    # skip encoding format line
                    if (line.find("<?xml") >= 0):
                        continue
                    # add line
                    addon_xml += line.rstrip() + "\n"
                    # find version and zip addon
                    if line.startswith("<addon"):
                        version = pattern.search(line).group(1)
                        output_file = f"{addon}-{version}"

                        with ZipFile(output_file, 'w') as zip_file:
                            for filename, filepath in walk_dir(addon):
                                # dont add existing releases to the next zip
                                if filename.endswith('.zip') and filename.startswith(addon):
                                    continue
                                if is_file_excluded(filename):
                                    continue
                                zip_file.write(filepath)

                            shutil.move(output_file, os.path.join(
                                addon, f"{output_file}.zip"))
                            print(f"Created zip: {output_file}.zip")

                # we succeeded so add to our final addons.xml text
                addons_xml += addon_xml.rstrip() + "\n\n"
            except Exception as e:
                # missing or poorly formatted addon.xml
                print("Excluding %s for %s" % (_path, e))
        # clean and add closing tag
        addons_xml = addons_xml.strip() + "\n</addons>\n"
        # save file
        self._save_file(addons_xml.encode("UTF-8"), file="addons.xml")

    def generate_md5_file(self):
        # create a new md5 hash
        m = hashlib.md5(
            open("addons.xml", "r", encoding="UTF-8").read().encode("UTF-8")).hexdigest()
        # save file
        try:
            self._save_file(m.encode("UTF-8"), file="addons.xml.md5")
        except Exception as e:
            # oops
            print(f"An error occurred creating addons.xml.md5 file!\n{e}")

    def _save_file(self, data, file):
        try:
            # write data to the file (use b for Python 3)
            open(file, "wb").write(data)
        except Exception as e:
            # oops
            print(f"An error occurred saving {file} file!\n{e}")


if (__name__ == "__main__"):
    # start
    generator = Generator()

    # generate files
    generator.generate_addons_file()
    generator.generate_md5_file()

    # notify user
    print("Finished updating addons xml and md5 files")
