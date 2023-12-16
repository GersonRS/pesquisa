import os
import pylab
from pycbc.psd import interpolate, inverse_spectrum_truncation
from pycbc.waveform import get_fd_waveform
from pycbc.filter import matched_filter
import numpy as np
from pycbc.filter import sigma
from pycbc.catalog import Merger
import Catalog
from pycbc.filter import highpass

window = 410.0
version = "dados-4Khz-janela-"+str(int(window))+"/"

for event in Catalog.events:
    merger = Merger(event)

    strain, stilde = {}, {}
    for ifo in ['L1', 'H1']:
        # Read the detector data and remove low frequency content
        strain[ifo] = merger.strain(ifo, sample_rate=int(4096))
        # Also create a frequency domain version of the data
        stilde[ifo] = strain[ifo].to_frequencyseries()

    psds = {}
    for ifo in ['L1', 'H1']:
        # Calculate a psd from the data. We'll use 2s segments in a median - welch style estimate
        # We then interpolate the PSD to the desired frequency step.
        psds[ifo] = interpolate(strain[ifo].psd(4), stilde[ifo].delta_f)

        # We explicitly control how much data will be corrupted by overwhitening the data later on
        # In this case we choose 2 seconds.
        psds[ifo] = inverse_spectrum_truncation(psds[ifo], 4 * strain[ifo].sample_rate,
                                                low_frequency_cutoff=15.0,
                                                trunc_method='hann')

    mass1 = merger.median1d("mass1", return_errors=True)
    mass2 = merger.median1d("mass2", return_errors=True)

    list_mass1 = np.arange(mass1[0] + mass1[1], mass1[0] + mass1[2], 1)
    list_mass2 = np.arange(mass2[0] + mass2[1], mass2[0] + mass2[2], 1)

    # Variables to store when we've found the max
    hmax, smax, tmax, mmax1, mmax2, nsnr = None, {}, {}, 0, 0, 0
    snrs = []
    for m1 in list_mass1:
        for m2 in list_mass2:
            # Generate a waveform with a given component mass; assumed equal mass, nonspinning
            hp, hc = get_fd_waveform(approximant="IMRPhenomD",
                                     mass1=m1, mass2=m2,
                                     f_lower=20, delta_f=stilde[ifo].delta_f)
            hp.resize(len(stilde[ifo]))
            hc.resize(len(stilde[ifo]))

            # Matched filter the data and find the peak
            max_snr, max_time = {}, {}
            for ifo in ['L1', 'H1']:
                snr = matched_filter(hp, stilde[ifo], psd=psds[ifo], low_frequency_cutoff=20.0)
                snr = snr.time_slice(merger.time - 1, merger.time + 1)
                _, idx = snr.abs_max_loc()

                # The complex SNR at the peak
                max_snr[ifo] = snr[idx]

                # The time of the peak
                max_time[ifo] = float(idx) / snr.sample_rate + snr.start_time

            network_snr = (abs(np.array(max_snr.values())) ** 2.0).sum() ** 0.5
            snrs.append(max_snr)

            if ifo == "H1":
                onda = hp
            else:
                onda = hc

            # Keep track of only the loudest peak
            if network_snr > nsnr:
                tmax, hmax, mmax1, mmax2, smax = max_time, onda, m1, m2, max_snr
                nsnr = network_snr

    # See the SNR as a function of the component mass. Notice where this peaks as it gives us
    # an estimate of what the parameters of the source system are. Note that masses
    # here are in the *detector* frame, so if the source is located far away, it will in
    # fact correspond to a lighter system due to cosmological redshift.
    print("We found the best Mass1=%s and Mass2=%s solar masses for Event %s  (detector frame)" % (mmax1, mmax2, event))


    for i, ifo in enumerate(['L1', 'H1']):
        dt = tmax[ifo] - stilde[ifo].start_time
        inj = hmax.cyclic_time_shift(dt)

        inj /= sigma(hmax, psd=psds[ifo], low_frequency_cutoff=20.0)
        inj *= smax[ifo]

        hoft = (stilde[ifo] / psds[ifo] ** 0.5).to_timeseries()

        white_data = hoft.highpass_fir(Catalog.data[event]['f_band'][0], 512).lowpass_fir(
            Catalog.data[event]['f_band'][1], 512)
        wd = white_data.time_slice(merger.time - .3, merger.time + .3)

        template = (inj / psds[ifo] ** 0.5).to_timeseries()
        template.start_time = hoft.start_time
        temp = template.time_slice(merger.time - .3, merger.time + .3)

        pylab.figure(figsize=(20, 15))
        pylab.subplot(3, 1, 1)
        pylab.plot(wd.sample_times, wd, label="Data")
        pylab.plot(temp.sample_times, temp, label="template")
        pylab.title("Event %s - %s | Mass1 = %s and Mass2 = %s" % (event, ifo, mmax1, mmax2))
        pylab.grid('on')
        pylab.xlabel('Time since {0:.2f}'.format(float(merger.time)))
        pylab.ylabel('whitened strain')
        pylab.legend(loc='upper left')

        zoom = hoft.time_slice(merger.time - .3, merger.time + .3)

        times, freqs, power = zoom.qtransform(.001, logfsteps=100, frange=(20, 512), qrange=(8, 8))

        pylab.subplot(3, 1, 2)
        pylab.pcolormesh(times, freqs, power, vmin=0, vmax=50)
        pylab.ylim(20, 512)
        pylab.title('Interferometer: %s' % ifo)
        pylab.xlabel('Time (s)')
        pylab.ylabel('Frequency (Hz)')
        pylab.xlim(times.min(), times.max())
        pylab.yscale('log')

        stilde2 = stilde[ifo] - inj

        hoft = (stilde2 / psds[ifo] ** 0.5).to_timeseries()

        zoom = hoft.time_slice(merger.time - .3, merger.time + .3)
        times, freqs, power = zoom.qtransform(.001, logfsteps=100, frange=(20, 512), qrange=(8, 8))

        pylab.subplot(3, 1, 3)
        pylab.pcolormesh(times, freqs, power, vmin=0, vmax=50)
        pylab.ylim(20, 512)
        pylab.title('Interferometer: %s' % ifo)
        pylab.xlabel('Time (s)')
        pylab.ylabel('Frequency (Hz)')
        pylab.xlim(times.min(), times.max())
        pylab.yscale('log')

        pylab.suptitle('Mass1 = %s | Mass2 = %s' % (mmax1, mmax2), fontsize=16)

        pylab.savefig(os.environ['HOME'] + "/pesquisa/" + version + event + "-" + ifo + ".png")

exit()
