########################################
#                                      
# Name: Zaid Yazadi
# Collaboration Statement: N/A
#
########################################

class ContentItem():
    def __init__(self, cid, size, header, content):
        self.cid = cid
        self.size = size
        self.header = header
        self.content = content

    def __str__(self):
        return ('CONTENT ID: {} SIZE: {} HEADER: {} CONTENT: {}'.format(self.cid, self.size, self.header, self.content))

    __repr__=__str__


class ContentNode():
    def __init__(self, content, nextNode = None):
        self.value = content
        self.next = nextNode

    def __str__(self):
        return ('CONTENT:{}\n'.format(self.value))

    __repr__=__str__

class CacheList():
    def __init__(self, size):
        self.head = None
        self.tail = None
        self.maxSize = size
        self.remainingSize = size
        self.numItems = 0

    def __str__(self):
        listString = ""
        current = self.head
        while current is not None:
            listString += "[" + str(current.value) + "]\n"
            current = current.next
        return ('REMAINING SPACE:{}\nITEMS:{}\nLIST:\n{}\n'.format(self.remainingSize, self.numItems, listString))     

    __repr__=__str__

    # Function that inserts newest ContentItem into CacheList
    # by first creating a ContentNode
    # Parameters: - content (ContentItem)
    #             - evictionPolicy (str)
    # return Nothing
    def put(self, content, evictionPolicy):
        new = ContentNode(content)
        if self.remainingSize > new.value.size:
            new.next = self.head
            self.head = new
            if not self.tail:
                self.tail = self.head.next
            self.remainingSize -= self.head.value.size
            self.numItems += 1
            return
        else:
            if evictionPolicy == 'lru':
                while self.remainingSize < new.value.size:
                    self.lruEvict()
            elif evictionPolicy == 'mru':
                while self.remainingSize < new.value.size:
                    self.mruEvict()
        new.next = self.head
        self.head = new
        if not self.tail:
            self.tail = self.head.next
        self.remainingSize -= self.head.value.size
        self.numItems += 1

    # Searches through list to find content with specific ID
    # Parameters: - cid (int)
    # returns: - id-specific content
    #          - None (id not found)
    def find(self, cid):
        cur = self.head
        while cur and cur.value.cid != cid:
            cur = cur.next
        return cur.value if cur else None

    # MRU Eviction algorithm that removes most recently used ContentNode (self.head)
    # returns Nothing
    def mruEvict(self):
        cur = self.head
        x = cur.value.size
        self.head, cur.next = self.head.next, None
        self.remainingSize += x
        self.numItems -= 1

    # LRU Eviction algorithm that removes least recently used ContentNode (self.tail)
    # returns nothing
    def lruEvict(self):
        cur = self.head
        try:
            while cur.next != self.tail:
                cur = cur.next
        except AttributeError:
            pass
        if self.numItems == 1:
            self.remainingSize += self.head.value.size
            self.head = None
            self.numItems -= 1
            return
        x = self.tail.value.size
        cur.next = None
        self.tail = cur
        self.remainingSize += x
        self.numItems -= 1
        if self.numItems == 1:
            self.tail = None

    # Clears contents of list by removing head and tail values
    # return "Cleared cache!" message
    def clear(self):
        self.head = None
        self.tail = None
        self.remainingSize = self.maxSize
        self.numItems = 0
        return "Cleared cache!"

class Cache():
    """
        >>> cache = Cache()
        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1003, 13, "Content-Type: 0", "0xD")
        >>> content3 = ContentItem(1008, 242, "Content-Type: 0", "0xF2")
        >>> content4 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content5 = ContentItem(1001, 51, "Content-Type: 1", "110011")
        >>> content6 = ContentItem(1007, 155, "Content-Type: 1", "10011011")
        >>> content7 = ContentItem(1005, 18, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content8 = ContentItem(1002, 14, "Content-Type: 2", "<html><h2>'PSU'</h2></html>")
        >>> content9 = ContentItem(1006, 170, "Content-Type: 2", "<html><button>'Click Me'</button></html>")
        >>> cache.insert(content1, 'lru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> cache.insert(content2, 'lru')
        'INSERTED: CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD'
        >>> cache.insert(content3, 'lru')
        'Insertion not allowed. Content size is too large.'
        >>> cache.insert(content4, 'lru')
        'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
        >>> cache.insert(content5, 'lru')
        'INSERTED: CONTENT ID: 1001 SIZE: 51 HEADER: Content-Type: 1 CONTENT: 110011'
        >>> cache.insert(content6, 'lru')
        'INSERTED: CONTENT ID: 1007 SIZE: 155 HEADER: Content-Type: 1 CONTENT: 10011011'
        >>> cache.insert(content7, 'lru')
        "INSERTED: CONTENT ID: 1005 SIZE: 18 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>"
        >>> cache.insert(content8, 'lru')
        "INSERTED: CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>"
        >>> cache.insert(content9, 'lru')
        "INSERTED: CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>"
        >>> cache
        L1 CACHE:
        REMAINING SPACE:177
        ITEMS:2
        LIST:
        [CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        <BLANKLINE>
        L2 CACHE:
        REMAINING SPACE:45
        ITEMS:1
        LIST:
        [CONTENT ID: 1007 SIZE: 155 HEADER: Content-Type: 1 CONTENT: 10011011]
        <BLANKLINE>
        <BLANKLINE>
        L3 CACHE:
        REMAINING SPACE:16
        ITEMS:2
        LIST:
        [CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>]
        [CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>]
        <BLANKLINE>
        <BLANKLINE>
        <BLANKLINE>
        >>> cache.hierarchy[0].clear()
        'Cleared cache!'
        >>> cache.hierarchy[1].clear()
        'Cleared cache!'
        >>> cache.hierarchy[2].clear()
        'Cleared cache!'
        >>> cache
        L1 CACHE:
        REMAINING SPACE:200
        ITEMS:0
        LIST:
        <BLANKLINE>
        <BLANKLINE>
        L2 CACHE:
        REMAINING SPACE:200
        ITEMS:0
        LIST:
        <BLANKLINE>
        <BLANKLINE>
        L3 CACHE:
        REMAINING SPACE:200
        ITEMS:0
        LIST:
        <BLANKLINE>
        <BLANKLINE>
        <BLANKLINE>
        >>> cache.insert(content1, 'mru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> cache.insert(content2, 'mru')
        'INSERTED: CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD'
        >>> cache.retrieveContent(content1)
        CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA
        >>> cache.retrieveContent(content2)
        CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD
        >>> cache.retrieveContent(content3)
        'Cache miss!'
        >>> cache.insert(content5, 'mru')
        'INSERTED: CONTENT ID: 1001 SIZE: 51 HEADER: Content-Type: 1 CONTENT: 110011'
        >>> cache.insert(content6, 'mru')
        'INSERTED: CONTENT ID: 1007 SIZE: 155 HEADER: Content-Type: 1 CONTENT: 10011011'
        >>> cache.insert(content4, 'mru')
        'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
        >>> cache.insert(content7, 'mru')
        "INSERTED: CONTENT ID: 1005 SIZE: 18 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>"
        >>> cache.insert(content8, 'mru')
        "INSERTED: CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>"
        >>> cache.insert(content9, 'mru')
        "INSERTED: CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>"
        >>> cache
        L1 CACHE:
        REMAINING SPACE:177
        ITEMS:2
        LIST:
        [CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        <BLANKLINE>
        L2 CACHE:
        REMAINING SPACE:150
        ITEMS:1
        LIST:
        [CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010]
        <BLANKLINE>
        <BLANKLINE>
        L3 CACHE:
        REMAINING SPACE:12
        ITEMS:2
        LIST:
        [CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>]
        [CONTENT ID: 1005 SIZE: 18 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>]
        <BLANKLINE>
        <BLANKLINE>
        <BLANKLINE>
    """
    def __init__(self):
        self.hierarchy = [CacheList(200) for _ in range(3)]
        self.size = 3
    
    def __str__(self):
        return ('L1 CACHE:\n{}\nL2 CACHE:\n{}\nL3 CACHE:\n{}\n'.format(self.hierarchy[0], self.hierarchy[1], self.hierarchy[2]))
    
    __repr__=__str__

    # Sums ASCII values of every symbol/letter/alphabet in content header
    # Finds the modulus of the sum and Cache size (3) to find correct CacheList
    # Collision is basically handled with separate chaining
    # returns sum % size (list index)
    def hashFunc(self, contentHeader):
        total = 0
        for c in contentHeader:
            total += ord(c)
        return total % self.size

    # Inserts the content into the cache using CacheList.put()
    # Parameters: - content (ContentItem)
    #             - evictionPolicy (str)
    # returns: - Inserted message
    #          - Insertion not allowed due to size message
    #          - None (incorrect parameter type)
    def insert(self, content, evictionPolicy):
        if type(content) == ContentItem:
            if content.size <= 200:
                self.hierarchy[self.hashFunc(content.header)].put(content, evictionPolicy)
                return "INSERTED: {}".format(content)
            else:
                return "Insertion not allowed. Content size is too large."
        else:
            return None

    # Searches through cache to find specified ContentItem
    # Parameters: - content(ContentItem)
    # returns: - specified content (if found)
    #          - "Cache miss!" message
    def retrieveContent(self, content):
        level = self.hashFunc(content.header)
        cur = self.hierarchy[level].head
        while cur and cur.value != content:
            cur = cur.next
        return cur.value if cur else "Cache miss!"
