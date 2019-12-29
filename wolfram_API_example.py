from ClientKeys import * # or ServerKeys
from NAPPS_Wolfram_API import *


WolframAPI = Wolfram_API()
WolframAPI.init(WOLFRAM_API_KEY)

WolframAPI.sendQuestion("How large is the Sun?")
ans = WolframAPI.returnAns()

print (ans)
