from __future__ import print_function
import functools
import multiprocessing
import subprocess
import sys


def light_the_candle(prj,  light_opts=[]):


    candle = ['candle.exe', '-arch' , "x${ARCH}", prj+'.wxs']
    light = ['light.exe', prj+'.wixobj'] + light_opts
    cp = subprocess.Popen(candle, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    candlecmd = ' '.join(candle)
    lightcmd  = ' '.join(light)

    candleout, err = cp.communicate()
    lightout = ''
    if 'error' not in candleout:
        lp = subprocess.Popen(light, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        lightout, err = lp.communicate()
    return prj, candlecmd, candleout, lightcmd, lightout






projects = [
%for dep in sorted(CALLING_PROJECT_DEPS.keys()): 
    "${dep}",
%endfor
]




if __name__ == '__main__':

    p = multiprocessing.Pool()

    apply_async = lambda x: p.apply_async(light_the_candle,[x])
    results = map(apply_async, projects )

    def process_output(args):
        prj, candlecmd, candleout, lightcmd, lightout = args
        print (candlecmd)
        if 'warning' in candleout or 'error' in candleout:
            print (candleout)
        print (lightcmd)
        if 'warning' in lightout or 'error' in lightout:
            print (lightout)

    while results:
        r = results.pop(0)
        try:
            process_output(r.get())
        except multiprocessing.TimeoutError:
            results.append(r)


    out = light_the_candle( '${CALLING_PROJECT_FULL_NAME}',
             light_opts=['-ext', 'WixUIExtension', '-cultures:en-us' ])
    process_output(out)

