import requests
import hashlib


class MinecraftApiTask:
    def __init__(self, username, password, taskname, call_args=[], tag=None):
        self.username = username
        self.taskname = taskname
        hasher = hashlib.sha256()
        hasher.update('{}{}{}'.format(
            username,
            taskname,
            password
        ).encode())
        self.taskhash = hasher.hexdigest()
        self.calling_args = call_args


class MinecraftApiWorker:
    def __init__(self, host, port, call_addr='/api/2/call'):
        self.__httpaddr = f'http://{host}:{port}{call_addr}'
        self.__queue = []

    def add_task(self, task):
        self.__queue.append(task)

    def compile_tasks(self, custom_queue=None):
        tasks = []
        if custom_queue == None:
            queue = self.__queue
        elif isinstance(custom_queue, list):
            queue = custom_queue
        else:
            raise TypeError('Wrong type of queue')
        for t in queue:
            tasks.append({
                'name': t.taskname,
                'key': t.taskhash,
                'username': t.username,
                'arguments': t.calling_args
            })
        return tasks

    def do_tasks(self):
        response = requests.post(
            self.__httpaddr,
            json=self.compile_tasks(),
        )
        return response.json()

    def run_task(self, task):
        response = requests.post(
            self.__httpaddr,
            json=self.compile_tasks(custom_queue=[task])
        )
        return response.json()[0]
