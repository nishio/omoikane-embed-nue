"""
entrypoint from github actions
"""

import scrapbox_io
import nue


def main(dry=False):
    pages = nue.main()
    scrapbox_io.write_pages(pages)
    print("write ok")


if __name__ == "__main__":
    main()
