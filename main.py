import optparse

import numpy as np

import CyclicCode as code

p = optparse.OptionParser()
p.add_option('--cx', '-c')
p.add_option('--message', '-m')
p.add_option('--error', '-e')
options, arguments = p.parse_args()
testQx = np.array(options.cx)

gX = options.cx.split(',')
gX = list(map(int, gX))

m = options.message.split(',')
m = list(map(int, m))

e = options.error.split(',')
e = list(map(int, e))

c = code.CyclicCode(gX)
res = c.code(m)
codedMsg = c.add_errors(e, res)
print("start msg = ", res)
print("error vec = ", np.array(e))
print("coded msg = ", codedMsg)
c1, c2, msg = c.alternative_decode(codedMsg)
if np.array_equal(c1, c2):
    E = 0
else:
    E = 1


print("E = ", E)
