'''
Exceptions
'''

class PagenationRangeIntegrityFailed(Exception):
    def __init__(self,limit,searched):
        super(PagenationRangeIntegrityFailed, self).__init__(f"Unable to set limit, by range error : Limit - {limit} Searched - {searched}")