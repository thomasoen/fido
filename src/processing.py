import time
import random
import logging
import requests
import parsing
import urls
from pymongo import Connection
import multiprocessing
from multiprocessing import Process

PROCESS_COUNT = multiprocessing.cpu_count() * 10


class WorkerPool(object):
    def __init__(self, function, arguments, count=PROCESS_COUNT):
        self.processes = []
        for i in xrange(count):
            self.processes.append(Process(target=function, args=arguments))

    def start(self):
        for process in self.processes:
            process.start()

    def join(self):
        for process in self.processes:
            process.join()

    def terminate(self):
        for process in self.processes:
            process.terminate()


def _create_process_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.FileHandler('%s.log' % name))
    return logger


def url_feeder_process(urlsFile, urlsQueue):
    logger = _create_process_logger('url_feeder_process')
    generator = urls.urls_generator(urlsFile)
    while True:
        try:
            url, proxy = generator.next()
            logger.info('Putting item in queue %s %s' % (url, proxy))
            urlsQueue.put((url, proxy))
        except StopIteration:
            break


def url_fetching_process(urlsQueue, outputQueue):
    logger = _create_process_logger('url_fetching_process')
    logger.info('Listening for items in the queue')
    while True:
        url, proxy = urlsQueue.get()
        logger.debug('Processing %s with %s' % (url, proxy))
        html = requests.get(url, proxies={'http': proxy}).text
        output = parsing.parse_html(html)
        outputQueue.put((url, output))
        time.sleep(random.randint(15, 45))


def html_persistance_process(outputQueue):
    conn = Connection()
    db = conn['crawler']
    logger = _create_process_logger('html_persistance_process')
    while True:
        url, data = outputQueue.get()
        if data and 'error' not in data:
            try:
                data['url'] = url
                data['epochstamp'] = int(time.time())
                db.bundle.insert(data)
            except Exception, e:
                logger.info('Error saving to mongodb %s' % str(e))
            logger.info('Saving dict to mongo as json ' + str(data))
        else:
            logger.info('Skiping due to ' + str(data))
