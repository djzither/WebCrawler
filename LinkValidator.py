class LinkValidator:
    def __init__(self, domain_name, lst):
        self.domain_name = domain_name
        self.lst = lst

    def can_follow_link(self, url):
        if not url.startswith(self.domain_name):
            return False     
        for path in self.lst:
            if url.startswith(self.domain_name+ path):
                return False

        return True
    