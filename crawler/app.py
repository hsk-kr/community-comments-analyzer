from crawling.community import dogdrip_scraper
import multiprocessing


def start_parse(page, next_page_step):
    scraper = dogdrip_scraper.DogdripScraper(
        page=page, next_page_step=next_page_step)
    while True:
        print(scraper.current_page)
        for p in scraper.posts:
            comments = p.comments
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

    # join processes
    for process in processes:
        process.join()
