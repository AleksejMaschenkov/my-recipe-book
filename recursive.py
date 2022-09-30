# -*- coding: utf-8 -*-


# ============================================================
#                  speed measurement
# ============================================================
import functools
import time


def log(text=''):
    """
    @log('MY EXAMPLE')
    def examp_test_sped(x, y):
        return x + y
    """

    def metric(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            t_begin = time.time()
            res = fn(*args, **kwargs)
            print(f'{text} {fn.__name__} executed in {(time.time() - t_begin) * 1000} ms')
            return res

        return wrapper

    return metric


# ============================================================
#                     RECURS
# ============================================================
@log('time')
def split_str(seq, chunk, skip_tail=False):
    """ seq=[1, 2, 5, 8, 555, 100000, 'xxxxx'] chunk=3 result: [[1, 2, 5], [8, 555, 100000], ['xxxxx']]
    
    
    seq=  "123456789abcdefghijAAAAHFRGЫРГОП лоилоилди" chunk=3
    result: ['12345', '6789a', 'bcdef', 'ghijA', 'AAAHF', 'RGЫРГ', 'ОП ло', 'илоил', 'ди']
    
    """
    lst = []
    if chunk <= len(seq):
        lst.extend([seq[:chunk]])
        lst.extend(split_str(seq[chunk:], chunk, skip_tail))
    elif not skip_tail and seq:
        lst.extend([seq])
    return lst


# ============================================================
#
# ============================================================
if __name__ == '__main__':
    @log('EXAMPLE decorator @log')
    def examp_test_sped(x, y):
        time.sleep(0.01)
        return x + y

    temp = examp_test_sped(20, 50)
    print('----------------------------------------------')
    
    mystr0 = [1, 2, 5, 8, 555, 100000, 'xxxxx']
    print(f'SRC:{mystr0}')
    print('result:', split_str(mystr0, 3))

    print('----------------------------------------------')
    mystr1 = "123456789abcdefghijAAAAHFRGЫРГОП лоилоилди"
    print(f'SRC:{mystr1}')
    print('result:', split_str(mystr1, 5))
    
"""

EXAMPLE decorator @log examp_test_sped executed in 9.999990463256836 ms
----------------------------------------------
SRC:[1, 2, 5, 8, 555, 100000, 'xxxxx']
time split_str executed in 0.0 ms
time split_str executed in 0.0 ms
time split_str executed in 0.0 ms
result: [[1, 2, 5], [8, 555, 100000], ['xxxxx']]
----------------------------------------------
SRC:123456789abcdefghijAAAAHFRGЫРГОП лоилоилди
time split_str executed in 0.0 ms
time split_str executed in 0.0 ms
time split_str executed in 0.0 ms
time split_str executed in 0.0 ms
time split_str executed in 0.0 ms
time split_str executed in 0.0 ms
time split_str executed in 0.0 ms
time split_str executed in 0.0 ms
time split_str executed in 0.0 ms
result: ['12345', '6789a', 'bcdef', 'ghijA', 'AAAHF', 'RGЫРГ', 'ОП ло', 'илоил', 'ди']

Process finished with exit code 0

"""
