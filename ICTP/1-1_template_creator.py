from eqcorrscan.utils.catalog_utils import filter_picks
from eqcorrscan.core.template_gen import from_meta_file
from obspy import read_events, read, Catalog
import glob

################################################

#Antelope QuakeMLs
path = 'quakeml/'
event_files = glob.glob(path + '*.xml')

################################################

#Set stations and chans you want to use
stations = ["JAVS", "SKDS", "CEY", "KNDS"]
chans = ["HHZ", "HHE", "HHN"]

################################################
cat = Catalog()
#Loop through original QuakeML files you got from Antelope with event2qml command
for event_file in event_files:
    cat += read_events(event_file)
print cat

#Filter and save original QuakeMLs into new QuakeMLs that you will use for template creation
filtered_catalog = filter_picks(catalog=cat, stations=stations, channels=chans, evaluation_mode=u'manual')

for event in filtered_catalog:
    print event
    event.write("quakeml_for_templates/"+str(event.origins[0].time)+".xml", format="QUAKEML")
    print "QuakeML for eqcorrscan's templates written."

#Template creation starts here

################################################

#QuakeMLs for templates
new_path = 'quakeml_for_templates/'
new_event_files = glob.glob(new_path + '*.xml')

################################################
new_catt = Catalog()
for new_event_file in new_event_files:
    new_catt += read_events(new_event_file)
new_catt.plot()

for new_event_file in new_event_files:

    new_cat = read_events(new_event_file)
    print new_cat

    julday = new_cat.events[0].origins[0].time.julday
    julday = str(julday)

    if len(julday) == 2:
        julday = '0'+julday
    if len(julday) == 1:
        julday = '00'+julday



    st = read("24h/"+julday+"/*")

    for tr in st:
        # Change channel names to two letters because EQcorrscan uses Seisan
        # style channel names, which are not standard, and should be changed!
        # Note that I might change EQcorrscan to use proper three letter
        # chanel names in a future release, but I will ensure it works with
        # two letter channel names too.
        tr.stats.channel = tr.stats.channel[0] + tr.stats.channel[-1]

    for tr in st:
        if tr.stats.station == "PRED":
            if tr.stats.sampling_rate != 100.0:
                tr.stats.sampling_rate=100.0
        elif tr.stats.station == "DRE_NI":
            if tr.stats.sampling_rate != 100.0:
                tr.stats.sampling_rate=100.0
        else:
            if tr.stats.sampling_rate != 200.0:
                tr.stats.sampling_rate = 200.0

    st.merge(method=1, fill_value=0)

    print st

    templates = from_meta_file(meta_file=new_event_file, st=st, lowcut=3.0, highcut=6.0, samp_rate=20.0,
                               filt_order=3, length=5, prepick=0.2, swin='all', all_horiz=True,
                               delayed=True, plot=False)

    for template in templates:
        template.write("templates/"+ str(new_cat.events[0].origins[0].time)+".mseed", format="MSEED")
