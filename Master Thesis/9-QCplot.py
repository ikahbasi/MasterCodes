import  myfunc.qcontrol_plot as qcontrol_plot
from obspy import read_events
import glob
from os.path import basename, join
from myfunc.parameters import parameters
params = parameters.QC()
basepath = params.Input
run_dirs = glob.glob(join(basepath, 'run*'))

inp = join(basepath, 'QC')
out = join(basepath, 'QC-plot')

target = 'rms'
print(target)
qcontrol_plot.hist_rms(path=join(inp, target, '*'),
                       outpath=join(out, target),
                       save=True, show=False, log=False)

#target = 'rms-clean'
#print(target)
#qcontrol_plot.hist_rms(path=join(inp, target, '*'),
#                       outpath=join(out, target),
#                       save=True, show=False)




target = 'phases-pre-event'
print(target)
qcontrol_plot.phase_pre_event(path=join(inp, target, '*'),
                              outpath=join(out, target),
                              save=True, show=False)

#target = 'phases-counter'
#print(target)
#qcontrol_plot.phase_counter(path=join(inp, target, '*'),
#                            outpath=join(out, target),
#                            save=True, show=False)

for target in ['n-cc']:#['cc', 'n-cc', 'scc']:
    print(target)
    qcontrol_plot.hist_correlation(path=join(inp, target, '*'),
                                   outpath=join(out, target),
                                   save=True, show=False)
target = 'n-scc'
print(target)
#qcontrol_plot.hist_correlation(path=join(inp, target, '*'), column=1,
#                               outpath=join(out, target+'_norm-on-phase'),
#                               save=True, show=False)
qcontrol_plot.hist_correlation(path=join(inp, target, '*'), column=2,
                               outpath=join(out, target+'_norm-on-template'),
                               save=True, show=False)
                               
target = 'self-detection'
print(target)
qcontrol_plot.self_detection(path=join(inp, target, '*'),
                             outpath=join(out, target),
                             save=True, show=False)



target = 'phases-pre-event-clean-catalog'
print(target)
qcontrol_plot.phase_pre_event(path=join(inp, target, '*'),
                              outpath=join(out, target),
                              save=True, show=False)

target = 'phases-counter-clean-catalog'
print(target)
qcontrol_plot.phase_counter(path=join(inp, target, '*'),
                            outpath=join(out, target),
                            save=True, show=False)
