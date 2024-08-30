def xcorr_pick_family(family, stream, shift_len=0.2, min_cc=0.4,
                      horizontal_chans=['E', 'N', '1', '2'],
                      vertical_chans=['Z'], cores=1, interpolate=False,
                      plot=False, plotdir=None):
    """
    Compute cross-correlation picks for detections in a family.

    :type family: `eqcorrscan.core.match_filter.family.Family`
    :param family: Family to calculate correlation picks for.
    :type stream: `obspy.core.stream.Stream`
    :param stream:
        Data stream containing data for all (or a subset of) detections in
        the Family
    :type shift_len: float
    :param shift_len:
        Shift length allowed for the pick in seconds, will be plus/minus this
        amount - default=0.2
    :type min_cc: float
    :param min_cc:
        Minimum cross-correlation value to be considered a pick, default=0.4.
    :type horizontal_chans: list
    :param horizontal_chans:
        List of channel endings for horizontal-channels, on which S-picks will
        be made.
    :type vertical_chans: list
    :param vertical_chans:
        List of channel endings for vertical-channels, on which P-picks will
        be made.
    :type cores: int
    :param cores:
        Number of cores to use in parallel processing, defaults to one.
    :type interpolate: bool
    :param interpolate:
        Interpolate the correlation function to achieve sub-sample precision.
    :type plot: bool
    :param plot:
        To generate a plot for every detection or not, defaults to False
    :type plotdir: str
    :param plotdir:
        Path to plotting folder, plots will be output here.

    :return: Catalog of events.
    """
    picked_dict = {}
    delta = family.template.st[0].stats.delta
    detect_streams_dict = _prepare_data(
        family=family, detect_data=stream, shift_len=shift_len)
    detection_ids = list(detect_streams_dict.keys())
    detect_streams = [detect_streams_dict[detection_id]
                      for detection_id in detection_ids]
    if len(detect_streams) == 0:
        Logger.warning("No appropriate data found, check your family and "
                       "detections - make sure seed ids match")
        return picked_dict
    if len(detect_streams) != len(family):
        Logger.warning("Not all detections have matching data. "
                       "Proceeding anyway. HINT: Make sure SEED IDs match")
    # Correlation function needs a list of streams, we need to maintain order.
    ccc, chans = _concatenate_and_correlate(
        streams=detect_streams, template=family.template.st, cores=cores)
    for i, detection_id in enumerate(detection_ids):
        detection = [d for d in family.detections if d.id == detection_id][0]
        correlations = ccc[i]
        picked_chans = chans[i]
        detect_stream = detect_streams_dict[detection_id]
        checksum, cccsum, used_chans = 0.0, 0.0, 0
        event = Event()
        for correlation, stachan in zip(correlations, picked_chans):
            if not stachan.used:
                continue
            tr = detect_stream.select(
                station=stachan.channel[0], channel=stachan.channel[1])[0]
            if interpolate:
                shift, cc_max = _xcorr_interp(correlation, dt=delta)
            else:
                cc_max = np.amax(correlation)
                shift = np.argmax(correlation) * delta
            if np.isnan(cc_max):  # pragma: no cover
                Logger.error(
                    'Problematic trace, no cross correlation possible')
                continue
            picktime = tr.stats.starttime + shift
            checksum += cc_max
            used_chans += 1
            
            ########### mine ###### start
            if cc_max > min_cc:
                _skip_phase = False
            elif cc_max < min_cc and shift_len >= 0.5:
                num_of_peaks = len(
                    find_peaks(correlation, height=0.75*cc_max)[0]
                    )
                if  num_of_peaks == 1 and cc_max > (min_cc/2):
                    _skip_phase = False
                else:
                    _skip_phase = True
            else:
                _skip_phase = True
            
            if _skip_phase:
                Logger.debug('Correlation of {0} is below threshold, not '
                             'using'.format(cc_max))
                continue
            ########### mine ###### end
            ########### origin ###### start
            #if cc_max < min_cc:
            #    Logger.debug('Correlation of {0} is below threshold, not '
            #                 'using'.format(cc_max))
            #    continue
            ########### origin ###### end
            cccsum += cc_max
            phase = None
            if stachan.channel[1][-1] in vertical_chans:
                phase = 'P'
            elif stachan.channel[1][-1] in horizontal_chans:
                phase = 'S'
            _waveform_id = WaveformStreamID(seed_string=tr.id)
            event.picks.append(Pick(
                waveform_id=_waveform_id, time=picktime,
                method_id=ResourceIdentifier('EQcorrscan'), phase_hint=phase,
                creation_info='eqcorrscan.core.lag_calc',
                evaluation_mode='automatic',
                comments=[Comment(text='cc_max={0}'.format(cc_max))]))
        event.resource_id = ResourceIdentifier(detection_id)
        event.comments.append(Comment(text="detect_val={0}".format(cccsum)))
        # Add template-name as comment to events
        event.comments.append(Comment(
            text="Detected using template: {0}".format(family.template.name)))
        if used_chans == detection.no_chans:  # pragma: no cover
            if detection.detect_val is not None and\
               checksum - detection.detect_val < -(0.3 * detection.detect_val):
                msg = ('lag-calc has decreased cccsum from %f to %f - '
                       % (detection.detect_val, checksum))
                Logger.error(msg)
                continue
        else:
            Logger.warning(
                'Cannot check if cccsum is better, used {0} channels for '
                'detection, but {1} are used here'.format(
                    detection.no_chans, used_chans))
        picked_dict.update({detection_id: event})
    if plot:  # pragma: no cover
        for i, event in enumerate(picked_dict.values()):
            if len(event.picks) == 0:
                continue
            plot_stream = detect_streams[i].copy()
            template_plot = family.template.st.copy()
            pick_stachans = [(pick.waveform_id.station_code,
                              pick.waveform_id.channel_code)
                             for pick in event.picks]
            for tr in plot_stream:
                if (tr.stats.station, tr.stats.channel) \
                        not in pick_stachans:
                    plot_stream.remove(tr)
            for tr in template_plot:
                if (tr.stats.station, tr.stats.channel) \
                        not in pick_stachans:
                    template_plot.remove(tr)
            if plotdir is not None:
                if not os.path.isdir(plotdir):
                    os.makedirs(plotdir)
                savefile = "{plotdir}/{rid}.png".format(
                    plotdir=plotdir, rid=event.resource_id.id)
                plot_repicked(template=template_plot, picks=event.picks,
                              det_stream=plot_stream, show=False, save=True,
                              savefile=savefile)
            else:
                plot_repicked(template=template_plot, picks=event.picks,
                              det_stream=plot_stream, show=True)
    return picked_dict
