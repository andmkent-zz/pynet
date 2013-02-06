
class Node:

    def __init__(self, name, link):
        self.name = name
        self.link = link
    
    def handle_message(self, t, message):
        message.nq_time = t
        self.link.enqueue(t, message)