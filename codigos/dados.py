import json
from astropy.utils.data import download_file
import numpy

# For the time being all quantities are the 1-d median value
# FIXME with posteriors when available and we can just post-process that

# GWTC-1 catalog
gwtc1_url = "https://www.gw-openscience.org/catalog/GWTC-1-marginal/filelist/"


def sliding_window(sequence, win_size, step=1):
    """Returns a generator that will iterate through
    the defined chunks of input sequence.  Input sequence
    must be iterable."""

    # Verify the inputs
    try:
        it = iter(sequence)
    except TypeError:
        raise Exception("**ERROR** sequence must be iterable.")
    if not ((type(0) == type(win_size)) and (type(step) == type(0))):
        raise Exception("**ERROR** type(winSize) and type(step) must be int.")
    if step > win_size:
        raise Exception("**ERROR** step must not be larger than winSize.")
    if win_size > len(sequence):
        raise Exception("**ERROR** winSize must not be larger than sequence length.")

    # Pre-compute number of chunks to emit
    num_of_chunks = ((len(sequence) - win_size) / step) + 1

    # Do the work
    for i in range(0, num_of_chunks * step, step):
        yield sequence[i:i + win_size]


def get_source(source):
    """Get the source data for a particular GW catalog
    """
    if source == 'gwtc-1':
        fname = download_file(gwtc1_url, cache=True)
        data = json.load(open(fname, 'r'))
    else:
        raise ValueError('Unkown catalog source {}'.format(source))
    return data['data']


class Merger(object):
    """Informaton about a specific compact binary merger"""

    def __init__(self, name, source='gwtc-1'):
        """ Return the information of a merger

        Parameters
        ----------
        name: str
            The name (GW prefixed date) of the merger event.
        """
        self.data = get_source(source)[name]

        # Set some basic params from the dataset
        for key in self.data:
            if 'best' in self.data[key]:
                setattr(self, key, self.data[key]['best'])

        self.time = self.data['tc']['best']

    def median1d(self, name, return_errors=False):
        """ Return median 1d marginalized parameters

        Parameters
        ----------
        name: str
            The name of the parameter requested
        return_errors: Optional, {bool, False}
            If true, return a second and third parameter that represents the
            lower and upper 90% error on the parameter.

        Returns
        -------
        param: float or tuple
            The requested parameter
        """
        if return_errors:
            mid = self.data[name]['best']
            low, high = self.data[name]['err']
            return (mid, low, high)
        else:
            return self.data[name]['best']

    def strain(self, ifo, duration=32, sample_rate=4096):
        """ Return strain around the event

        Currently this will return the strain around the event in the smallest
        format available. Selection of other data is not yet available.

        Parameters
        ----------
        ifo: str
            The name of the observatory you want strain for. Ex. H1, L1, V1

        Returns
        -------
        strain: pycbc.types.TimeSeries
            Strain around the event.
        """
        from astropy.utils.data import download_file
        from pycbc.frame import read_frame

        # Information is currently wrong on GWOSC!
        # channels = self.data['files']['FrameChannels']
        # for channel in channels:
        #    if ifo in channel:
        #        break

        length = "{}sec".format(duration)
        if sample_rate == 4096:
            sampling = "4KHz"
        elif sample_rate == 16384:
            sampling = "16KHz"

        channel = "{}:GWOSC-{}_R1_STRAIN".format(ifo, sampling.upper())
        url = self.data['files'][ifo][length][sampling]['GWF']
        filename = download_file(url, cache=True)
        return read_frame(str(filename), str(channel))


class Catalog(object):
    """Manage a set of binary mergers"""

    def __init__(self, source='gwtc-1'):
        """ Return the set of detected mergers

        The set of detected mergers. At some point this may have some selection
        abilities.
        """
        self.data = get_source(source=source)
        self.mergers = {name: Merger(name, source=source) for name in self.data}
        self.names = self.mergers.keys()

    def __len__(self):
        return len(self.mergers)

    def __getitem__(self, key):
        return self.mergers[key]

    def __setitem__(self, key, value):
        self.mergers[key] = value

    def __delitem__(self, key):
        del self.mergers[key]

    def __iter__(self):
        return iter(self.mergers)

    def median1d(self, param, return_errors=False):
        """ Return median 1d marginalized parameters

        Parameters
        ----------
        name: str
            The name of the parameter requested
        return_errors: Optional, {bool, False}
            If true, return a second and third parameter that represents the
            lower and upper 90% error on the parameter.

        Returns
        -------
        param: nump.ndarray or tuple
            The requested parameter
        """
        v = [self.mergers[m].median1d(param, return_errors=return_errors) for m in self.mergers]
        if return_errors:
            value, merror, perror = zip(*v)
            return numpy.array(value), numpy.array(merror), numpy.array(perror)
        else:
            return numpy.array(v)


c = Catalog()

from pycbc.frame import read_frame
from pycbc.filter import highpass_fir, lowpass_fir
from pycbc.waveform import get_fd_waveform
from pycbc.psd import welch, interpolate, inverse_spectrum_truncation
import pylab
import h5py
import os

window = 410.0
version = "dados-4Khz-janela-marginal-" + str(int(window)) + "/"

for event in c.names:
    merger = c.mergers[event]
    pylab.figure(figsize=[15, 8])
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

            sliding_data = numpy.array(list(sliding_window(white_data, int(window))))
            archive.create_dataset(ifo, data=sliding_data)

        print "archive " + archive.filename + " successfully generated."
        archive.close()
    pylab.savefig(os.environ['HOME'] + "/pesquisa/" + version + event + ".png")

exit()
