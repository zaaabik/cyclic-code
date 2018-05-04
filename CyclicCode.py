import numpy as np


class CyclicCode(object):
    def __init__(self, polynomial):
        self.polynomial = polynomial
        self.r = len(polynomial) - np.min(np.nonzero(polynomial)) - 1
        self.booleanMapper = np.vectorize(get_zero_and_one)

    def code(self, m):
        print("data =", np.array(m))
        cx = np.array(m)
        cx = np.append(cx, [0] * self.r)
        cx = self.get_module(cx, self.polynomial)
        dif = self.r - len(cx)
        print("cx = ", cx)
        if dif != 0:
            cx = np.append([0] * dif, cx)
        return np.append(m, cx)

    def add_errors(self, e, m):
        diff = len(m) - len(e)
        e = np.array(np.append(e, [0] * diff), 'int')
        return self.booleanMapper(np.logical_xor(m, e))

    def decode(self, m):
        return m[:-self.r], self.get_module(m, self.polynomial)

    def alternative_decode(self, m):
        msg = m[:-self.r]
        cx = np.array(msg)
        cx = np.append(cx, [0] * self.r)
        cx = self.get_module(cx, self.polynomial)
        cb2 = m[-self.r:]
        dif = len(m[-self.r:]) - len(cx)
        cx = np.append(dif * [0], cx)
        print("msg = ", msg)
        print("cx2 = ", np.array(list(map(int, cx))))
        return cx, cb2, msg

    def get_module(self, p, module):
        if len(np.nonzero(p)[0]) == 0:
            return [0]
        p = np.array(p)
        module = np.array(module)
        p_deg = len(p) - np.min(np.nonzero(p)) - 1
        mod_deg = len(module) - np.min(np.nonzero(module)) - 1
        p = np.delete(p, range(0, np.min(np.nonzero(p))))
        module = np.delete(module, range(0, np.min(np.nonzero(module))))
        try:
            while p_deg >= mod_deg:
                deg = p_deg - mod_deg
                tmp_module = np.append(module, [0] * deg)
                p = np.logical_xor(p, tmp_module)
                p_deg = len(p) - np.min(np.nonzero(p)) - 1
                p = np.delete(p, range(0, np.min(np.nonzero(p))))
            v_func = np.vectorize(get_zero_and_one)
            return v_func(p)
        except ValueError:
            return [0]


def get_zero_and_one(y):
    if y == 1:
        return 1
    else:
        return 0
