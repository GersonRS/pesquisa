from pycbc.catalog import Catalog
from pycbc.psd import welch, interpolate, inverse_spectrum_truncation
import pylab
import h5py
import os

version = "aaaaa"

for event in Catalog().names:
    merger = Catalog().mergers[event]
    with h5py.File(os.environ['HOME'] + "/pesquisa/" + version + event + ".h5", "w") as archive:
        for i, ifo in enumerate(["L1", "H1"]):
            strain = merger.strain(ifo)
            stilde = strain.to_frequencyseries()

            psd = interpolate(strain.psd(4), stilde.delta_f)

            psd = inverse_spectrum_truncation(psd, 4 * strain.sample_rate,
                                              low_frequency_cutoff=15.0,
                                              trunc_method='hann')

            white_data = (stilde / psd ** 0.5).to_timeseries()

            white_data = white_data.highpass_fir(45, 512).lowpass_fir(300, 512)
            wd = white_data.time_slice(merger.time - .3, merger.time + .3)
            white_data = white_data.time_slice(merger.time - 1, merger.time + 1)

            if ifo is "H1":
                white_data = (white_data - (-68.21821870442363)) / (64.9621146587913 - (-68.21821870442363))
            else:
                white_data = (white_data - (-126.21782146064886)) / (139.25812657273104 - (-126.21782146064886))

            pylab.subplot(2, 2, (1 * 2) - i)
            pylab.plot(wd.sample_times, wd, label="Data")
            pylab.title("Event %s - %s" % (event, ifo))
            pylab.grid('on')
            pylab.xlabel('Time since {0:.2f}'.format(float(merger.time)))
            pylab.ylabel('whitened strain')
            pylab.legend(loc='upper left')

            hoft = (stilde / psd ** 0.5).to_timeseries()

            zoom = hoft.time_slice(merger.time - .3, merger.time + .3)

            times, freqs, power = zoom.qtransform(.001, logfsteps=100, frange=(20, 512), qrange=(4, 8))

            pylab.subplot(2, 2, (2 * 2) - i)
            pylab.pcolormesh(times, freqs, power, vmin=0, vmax=50)
            pylab.ylim(20, 512)
            pylab.title("%s original - %s" % (event, ifo))
            pylab.xlabel('Time (s)')
            pylab.ylabel('Frequency (Hz)')
            pylab.xlim(times.min(), times.max())
            pylab.yscale('log')

            # sliding_data = numpy.array(list(sliding_window(white_data, int(window))))
            archive.create_dataset(ifo, data=white_data)

        print "archive " + archive.filename + " successfully generated."
        archive.close()

exit()