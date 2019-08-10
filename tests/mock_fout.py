class MockFout:
    
    def __init__(self):
        self.record = []
    
    def write(self, s):
        self.record.append(s.rstrip())
    
    def flush(self):
        return
