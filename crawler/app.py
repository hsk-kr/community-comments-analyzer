import multiprocessing
from datetime import datetime
import time

from crawling.community import dogdrip_scraper
from es.dogdrip_es_helper import DogdripESHelper


LOG_FILE_PATH = "log/scraper_{0}.log".format(
    time.mktime(datetime.now().timetuple()))


def log(page, postnum):
    with open(LOG_FILE_PATH, "a") as f:
        f.write("page:{0} / postnum:{1} / time:{2}\n".format(page,
                                                             postnum, str(datetime.now())))


def start_parse(page, next_page_step):
    scraper = dogdrip_scraper.DogdripScraper(
        page=page, next_page_step=next_page_step)
    des = DogdripESHelper()

    while True:
        for p in scraper.posts:
            log(scraper.current_page, p.num)
            des.index_comments(p.num, p.comments)
        scraper.next_page()


if __name__ == "__main__":
    # over two isn't accepted by dogdrip. because request is too fast.
    processes_count = 2
    processes = []

    # spawn processes
    for i in range(1, processes_count+1):
        p = multiprocessing.Process(target=start_parse, kwargs=dict(
            page=i, next_page_step=processes_count))
        processes.append(p)
        p.start()

    print("Start parsing...")

    # join processes
    for process in processes:
        process.join()
