import sys

def get_arg(key):
    if key in sys.argv:
        print(sys.argv)
        value = sys.argv[sys.argv.index(key) + 1]
        print(f'{key} set to {value} index:{sys.argv.index(key) + 1}')
    else:
        print(f'{key} set to None.')
        value = None
    return value

Input = output = get_arg('--inp_out')
cores = 10
plot = False

class parameters():    
    class tribes():
        def __init__(self):
            # logging
            self.log_level = 'INFO'
            # routine
            self.Input_catalog = '../catalog'
            self.Input_stream = '../days'
            self.output = Input
            # select_proper_events
            self.min_num_stations = 3
            self.min_azimuthal_gap = 180
            # Tribe.construct
            self.lowcut = float(get_arg('--lowcut'))
            self.highcut = float(get_arg('--highcut'))
            self.samp_rate = 100.0
            self.filt_order = 4
            self.length = 1.1
            self.prepick = 0.1
            self.swin = 'all'
            self.all_horiz = False
            self.delayed = True
            self.min_snr = None
            self.plot = plot
            self.debug = 0
            self.parallel = True
            self.num_cores = cores
            self.skip_short_chans = False
        def __str__(self):
            out = f"{'-' * 55}\n"
            for key, val in self.__dict__.items():
                out += f"* {key:<25}{'|':<10}{str(val):<20}*\n"
                out += f"{'-' * 55}\n"
            return out

    
    class detect():
        def __init__(self):
            # logging
            self.log_level = 'INFO'
            # routine
            self.Input = Input
            self.output = output
            self.Input_stream = '../days'
            # tribe.detect
            self.threshold = 10
            self.threshold_type = 'MAD'
            self.trig_int = 6
            self.plot = plot
            self.daylong = True
            self.parallel_process = True
            self.cores = cores
            self.ignore_length = False
            self.ignore_bad_data = False
            self.group_size = 210
            self.overlap = 'calculate'
            self.full_peaks = False
            self.save_progress = False
            self.process_cores = None
            # decluster-parameter
            self.trig_int_decluster = 0.5
            self.timing = 'detect'  # ‘detect’ or ‘origin’
            self.metric = 'avg_cor'  # ‘avg_cor’ or ‘cor_sum’
        def __str__(self):
            out = f"{'-' * 55}\n"
            for key, val in self.__dict__.items():
                out += f"* {key:<25}{'|':<10}{str(val):<20}*\n"
                out += f"{'-' * 55}\n"
            return out

    class lag_calc():
        def __init__(self):
            # logging
            self.log_level = 'INFO'
            # routine
            self.Input = Input
            self.output = output
            self.Input_stream = '../days'
            # read party
            self.read_detection_catalog = False
            self.estimate_origin = True
            # decluster-parameter
            self.trig_int = 6
            self.timing = 'detect'  # ‘detect’ or ‘origin’
            self.metric = 'avg_cor'  # ‘avg_cor’ or ‘cor_sum’
            # party.lag_calc
            self.pre_processed = False
            self.shift_len = 0.5
            self.min_cc = 0.6
            self.cores = cores
            self.interpolate = False
            self.plot = plot
            self.parallel = True
            self.ignore_length = True
            self.ignore_bad_data = False
            self.relative_magnitudes = False
            # party.min_chans
            self.min_chans = 4
        def __str__(self):
            out = f"{'-' * 55}\n"
            for key, val in self.__dict__.items():
                out += f"* {key:<25}{'|':<10}{str(val):<20}*\n"
                out += f"{'-' * 55}\n"
            return out

    class get_cat():
        def __init__(self):
            # routine
            self.Input = Input
            self.output = output
            # party.min_chans
            self.min_chans = 4
            # type of output
            self.nordic = True
            self.quakeml = False
            self.nlloc = False
        def __str__(self):
            out = f"{'-' * 55}\n"
            for key, val in self.__dict__.items():
                out += f"* {key:<25}{'|':<10}{str(val):<20}*\n"
                out += f"{'-' * 55}\n"
            return out

    class cumulative():
        def __init__(self):
            # routine
            self.Input = Input
            self.output = output
            # party.min_chans(min_chans)
            self.min_chans = 4
        def __str__(self):
            out = f"{'-' * 55}\n"
            for key, val in self.__dict__.items():
                out += f"* {key:<25}{'|':<10}{str(val):<20}*\n"
                out += f"{'-' * 55}\n"
            return out

    class relative_magnitude():
        def __init__(self):
            # routine
            self.Input_stream = '../days'
            self.output = output
            self.Input = Input
            # pre-processing
            self.parallel = True
            self.cores = False    # if set to False use all cores
            self.lowcut = None       # if set to None use same as tribe params
            self.highcut = None      # if set to None use same as tribe params
            self.filt_order = None   # if set to None use same as tribe params
            # relative_magnitude function
            self.use_cc_of_lag = False
            self.noise_window = (-6, 0)
            self.signal_window = (-0.5, 10)
            self.min_snr = 1.0
            self.min_cc = 0.8
            self.use_s_picks = False
            self.shift = 0.2
            self.return_correlations = True
            self.weight_by_correlation = True
        def __str__(self):
            out = f"{'-' * 55}\n"
            for key, val in self.__dict__.items():
                out += f"* {key:<25}{'|':<10}{str(val):<20}*\n"
                out += f"{'-' * 55}\n"
            return out

    class Gutenberg_Richter():
        def __init__(self):
            # routine
            self.Input = Input
            self.output = output
            # select_proper_events
            self.min_num_stations = 3
            self.min_azimuthal_gap = 180
            self.path_refrence_catalog = '../catalog'
        def __str__(self):
            out = f"{'-' * 55}\n"
            for key, val in self.__dict__.items():
                out += f"* {key:<25}{'|':<10}{str(val):<20}*\n"
                out += f"{'-' * 55}\n"
            return out
    
    class QC():
        def __init__(self):
            self.Input = Input
            self.output = output
