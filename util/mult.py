from multiprocessing import Lock, Process, Queue, Value


class Mult:
    def __init__(self, keyword: str, max: int, uuid: str):
        self.keyword = keyword
        self.max = max
        self.lock = Lock()
        self.sum = Value("i", 0)
        self.q = Queue()

        self.uuid = uuid

    def create_process(self, crawler, process: int):
        procs = []

        p1 = Process(target=crawler().get_url, args=(self.keyword, self.max, self.q))
        p1.start()

        for i in range(0, process):
            print(f"process {i+1} strat")
            proc = Process(target=crawler().get_data, args=(self.sum, self.max, self.q, self.lock, self.uuid))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

        print(f"process end")
