import os
from scipy.stats import norm
import h5py
import pylab
from pycbc.psd import interpolate, inverse_spectrum_truncation
from pycbc.waveform import get_fd_waveform
from pycbc.filter import matched_filter
import numpy as np
from pycbc.filter import sigma
from pycbc.catalog import Merger
import Catalog

data_set = []
noise_set = []
templates = []
residuals = []
MUS = []
SIGMAS = []
fs = 1.0
window = 410.0
version = "dados-4Khz-janela-"+str(int(window))+"/"

for event in Catalog.events[9:]:
    merger = Merger(event)
    pylab.figure(figsize=[15, 8])
    with h5py.File(os.environ['HOME'] + "/pesquisa/" + version + event + ".h5", "w") as archive:
        for i, ifo in enumerate(["L1", "H1"]):
            strain = merger.strain(ifo, sample_rate=int(4096 * fs))
            stilde = strain.to_frequencyseries()

            psd = interpolate(strain.psd(4), stilde.delta_f)

            psd = inverse_spectrum_truncation(psd, 4 * strain.sample_rate,
                                              low_frequency_cutoff=15.0,
                                              trunc_method='hann')

            m1 = Catalog.data[event]['mass1']
            m2 = Catalog.data[event]['mass2']

            hp, hc = get_fd_waveform(approximant="IMRPhenomD",
                                     mass1=m1, mass2=m2,
                                     f_lower=20, delta_f=stilde.delta_f)

            hp.resize(len(stilde))
            hc.resize(len(stilde))

            if ifo is "H1":
                wave = hp
            else:
                wave = hc

            snr = matched_filter(wave, stilde, psd=psd, low_frequency_cutoff=20.0)
            snr = snr.crop(4 + 4, 4)
            _, idx = snr.abs_max_loc()

            time = float(idx) / snr.sample_rate + snr.start_time

            network_snr = (abs(np.array(snr[idx])) ** 2.0).sum() ** 0.5

            white_data = (stilde / psd ** 0.5).to_timeseries()
            white_data = white_data.highpass_fir(Catalog.data[event]['f_band'][0], 512).lowpass_fir(
                Catalog.data[event]['f_band'][1], 512)
            wd = white_data.time_slice(time - .3, time + .3)
            white_data = white_data.time_slice(time - 1, time + 1)

            dt = time - stilde.start_time
            inj = wave.cyclic_time_shift(dt)

            inj /= sigma(wave, psd=psd, low_frequency_cutoff=20.0)
            inj *= snr[idx]

            template = (inj / psd ** 0.5).to_timeseries()
            template.start_time = strain.start_time
            temp = template.time_slice(time - .3, time + .3)
            template = template.time_slice(time - 1, time + 1)
            if ifo is "H1":
                white_data = (white_data - (-138.46055191922176)) / (136.30964748604285 - (-138.46055191922176))
                template = (template - (-138.46055191922176)) / (136.30964748604285 - (-138.46055191922176))
            else:
                white_data = (white_data - (-126.21782146064886)) / (139.25812657273104 - (-126.21782146064886))
                template = (template - (-126.21782146240336)) / (139.2581265719687 - (-126.21782146240336))

            if event != "GW170818":
                templates.append(template)
                residual = white_data - template
                residuals.append(residual)

            pylab.subplot(3, 2, (1 * 2) - i)
            pylab.plot(wd.sample_times, wd, label="Data")
            pylab.plot(temp.sample_times, temp, label="template")
            pylab.title("Event %s - %s" % (event, ifo))
            pylab.grid('on')
            pylab.xlabel('Time since {0:.2f}'.format(float(merger.time)))
            pylab.ylabel('whitened strain')
            pylab.legend(loc='upper left')

            hoft = (stilde / psd ** 0.5).to_timeseries()

            zoom = hoft.time_slice(time - .3, time + .3)

            times, freqs, power = zoom.qtransform(.001, logfsteps=100, frange=(20, 512), qrange=(4, 8))

            pylab.subplot(3, 2, (2 * 2) - i)
            pylab.pcolormesh(times, freqs, power, vmin=0, vmax=50)
            pylab.ylim(20, 512)
            pylab.title("%s original - %s" % (event, ifo))
            pylab.xlabel('Time (s)')
            pylab.ylabel('Frequency (Hz)')
            pylab.xlim(times.min(), times.max())
            pylab.yscale('log')

            dt = time - stilde.start_time
            inj = wave.cyclic_time_shift(dt)

            inj /= sigma(wave, psd=psd, low_frequency_cutoff=20.0)
            inj *= snr[idx]

            stilde2 = stilde - inj
            hoft = (stilde2 / psd ** 0.5).to_timeseries()

            zoom = hoft.time_slice(time - .3, time + .3)
            times, freqs, power = zoom.qtransform(.001, logfsteps=100, frange=(20, 512), qrange=(4, 8))

            pylab.subplot(3, 2, (3 * 2) - i)
            pylab.pcolormesh(times, freqs, power, vmin=0, vmax=50)
            pylab.ylim(20, 512)
            pylab.title('%s subtract the template - %s' % (event, ifo))
            pylab.xlabel('Time (s)')
            pylab.ylabel('Frequency (Hz)')
            pylab.xlim(times.min(), times.max())
            pylab.yscale('log')
            sliding_data = np.array(list(Catalog.sliding_window(white_data, int((window * fs)))))
            archive.create_dataset(ifo, data=sliding_data)

        print "archive " + archive.filename + " successfully generated."
        archive.close()
    pylab.savefig(os.environ['HOME'] + "/pesquisa/" + version + event + ".png")

# for r in residuals:
#     (mu, sig) = norm.fit(r)
#     MUS.append(mu)
#     SIGMAS.append(sig)
#
# MU = np.array(MUS).mean()
# SIGMA = np.array(SIGMAS).mean()
#
# for temp in templates:
#     for ii in range(0, 300):
#         num = np.random.randint(int((50*(fs/4))*(window/410)), int((500*(fs/4))*(window/410)))
#         index_max = int(np.argmax(temp))
#         index = np.append(np.arange((index_max - (int(window/2)*int(fs))) - num, index_max - num, 1),
#                           np.arange(index_max - num, (index_max + (int(window/2)*int(fs))) - num, 1))
#         new = temp[index]
#         ruido = (np.random.normal(MU, SIGMA, len(new)))
#         data_set.append((new - min(new)) / (max(new) - min(new)))
#         noise_set.append((ruido - min(ruido)) / (max(ruido) - min(ruido)))
#
# all_of = []
# for i in range(len(data_set)):
#     data_base = np.append(np.array(data_set[i]), [1, 0], axis=0)
#     noise_base = np.append(np.array(noise_set[i]), [0, 1], axis=0)
#     all_of.append(data_base)
#     all_of.append(noise_base)
#
# all_of = np.array(all_of)
# np.random.shuffle(all_of)
#
# with h5py.File(os.environ['HOME'] + "/pesquisa/" + version + "data.h5", "w") as archive:
#     archive.create_dataset("X", data=all_of[:, :-2])
#     archive.create_dataset("t", data=all_of[:, -2:])
#     print "archive " + archive.filename + " successfully generated."
#     archive.close()
