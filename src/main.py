
import processing
from multiprocessing import Process, Queue

URLS_FILE_PATH = 'all_urls.txt'


def main():
    urlsQueue = Queue(1000)
    outputQueue = Queue(1000)

    # 1 feeder should be enough
    urlFeederProcess = Process(target=processing.url_feeder_process,
        args=(URLS_FILE_PATH, urlsQueue))

    # Default size in processing module is 10 per core/processor
    processingPool = processing.WorkerPool(processing.url_fetching_process,
        (urlsQueue, outputQueue))

    # We don't want too many processes saving to same database at the same time
    htmlPersistanceProcess = Process(target=processing.html_persistance_process,
        args=(outputQueue, ))

    try:
        urlFeederProcess.start()
        processingPool.start()
        htmlPersistanceProcess.start()

        #Wait for all processes to finish
        urlFeederProcess.join()
        processingPool.join()
        htmlPersistanceProcess.join()
    except Exception as detail:
        print("Shutting down processes because %s" % str(detail))
    finally:
        urlFeederProcess.terminate()
        processingPool.terminate()
        htmlPersistanceProcess.terminate()

if __name__ == '__main__':
    main()
