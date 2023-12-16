import os
from scipy.stats import norm
import pylab
import csv
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
version = "dados-4Khz-janela-" + str(int(window)) + "/"

for event in Catalog.events:
    merger = Merger(event)
    pylab.figure(figsize=[15, 8])
    pylab.subplots_adjust(hspace=0.5)
    for i, ifo in enumerate(["H1", "L1"]):
        w = csv.writer(open(os.environ['HOME'] + "/pesquisa/" + version + event + "-" + ifo + "-filter.csv", "wb"))
        d = csv.writer(open(os.environ['HOME'] + "/pesquisa/" + version + event + "-" + ifo + "-no-filter.csv", "wb"))
        r = csv.writer(open(os.environ['HOME'] + "/pesquisa/" + version + event + "-" + ifo + "-noise.csv", "wb"))
        strain = merger.strain(ifo, sample_rate=int(4096 * fs))
        stilde = strain.to_frequencyseries()

        psd = interpolate(strain.psd(4), stilde.delta_f)

        psd = inverse_spectrum_truncation(psd, 4 * strain.sample_rate,
                                          low_frequency_cutoff=15.0,
                                          trunc_method='hann')

        m1 = Catalog.data[event]['mass1']
        m2 = Catalog.data[event]['mass2']

        # m1 = merger.median1d("mass1")
        # m2 = merger.median1d("mass2")

        hp, hc = get_fd_waveform(approximant="IMRPhenomD",
                                 mass1=m1, mass2=m2,
                                 f_lower=20, delta_f=stilde.delta_f)

        hp.resize(len(stilde))
        hc.resize(len(stilde))

        if ifo is "H1":
            wave_template = hp
        else:
            wave_template = hc

        snr = matched_filter(wave_template, stilde, psd=psd, low_frequency_cutoff=20.0)
        snr = snr.crop(4 + 4, 4)
        _, idx = snr.abs_max_loc()

        time = float(idx) / snr.sample_rate + snr.start_time

        network_snr = (abs(np.array(snr[idx])) ** 2.0).sum() ** 0.5

        white_data = (stilde / psd ** 0.5).to_timeseries()
        white_data = white_data.highpass_fir(Catalog.data[event]['f_band'][0], 512).lowpass_fir(
            Catalog.data[event]['f_band'][1], 512)
        wd = white_data.time_slice(merger.time - .3, merger.time + .3)
        white_data_temp = white_data.time_slice(merger.time - 0.5, merger.time + 0.5)
        white_data = white_data.time_slice(merger.time - 1, merger.time + 1)

        dt = time - stilde.start_time
        inj = wave_template.cyclic_time_shift(dt)

        inj /= sigma(wave_template, psd=psd, low_frequency_cutoff=20.0)
        inj *= snr[idx]

        template = (inj / psd ** 0.5).to_timeseries()
        template.start_time = strain.start_time
        temp = template.time_slice(merger.time - .3, merger.time + .3)
        template = template.time_slice(merger.time - 1, merger.time + 1)
        if ifo is "H1":
            white_data = (white_data - (-138.46055191922176)) / (136.30964748604285 - (-138.46055191922176))
            template = (template - (-138.46055191922176)) / (136.30964748604285 - (-138.46055191922176))
        else:
            white_data = (white_data - (-126.21782146064886)) / (139.25812657273104 - (-126.21782146064886))
            template = (template - (-126.21782146240336)) / (139.2581265719687 - (-126.21782146240336))

        templates.append(template)
        residual = white_data - template
        residuals.append(residual)

        for dado1 in white_data_temp:
            w.writerow([dado1])
        for dado2 in strain.time_slice(merger.time - 0.5, merger.time + 0.5):
            d.writerow([dado2])
        for dado3 in strain[8192:12288]:
            r.writerow([dado3])

        pylab.subplot(3, 2, (1 * 2) - i)
        pylab.plot(white_data_temp.sample_times, white_data_temp, label="Data")
        # pylab.plot(temp.sample_times, temp, label="template")
        # pylab.subplot(1, 2, 1 + i)
        # pylab.plot(strain.sample_times, strain, label="Data")
        pylab.title("Data with Filter %s - %s" % (event, ifo))
        pylab.grid('on')
        pylab.xlabel('Time since {0:.2f}'.format(float(merger.time)))
        pylab.ylabel('whitened strain')
        pylab.legend(loc='upper left')

        hoft = (stilde / psd ** 0.5).to_timeseries()

        zoom = hoft.time_slice(merger.time - .3, merger.time + .3)

        # times, freqs, power = zoom.qtransform(.001, logfsteps=100, frange=(20, 512), qrange=(4, 8))

        pylab.subplot(3, 2, (2 * 2) - i)
        # pylab.pcolormesh(times, freqs, power, vmin=0, vmax=50)
        pylab.plot(strain.time_slice(merger.time - 0.5, merger.time + 0.5).sample_times,
                   strain.time_slice(merger.time - 0.5, merger.time + 0.5), label="Data")
        # pylab.ylim(20, 512)
        pylab.title("Data no Filter of %s - %s" % (event, ifo))
        # pylab.xlabel('Time (s)')
        # pylab.ylabel('Frequency (Hz)')
        # pylab.xlim(times.min(), times.max())
        # pylab.yscale('log')

        # dt = time - stilde.start_time
        # inj = wave_template.cyclic_time_shift(dt)
        #
        # inj /= sigma(wave_template, psd=psd, low_frequency_cutoff=20.0)
        # inj *= snr[idx]
        #
        # stilde2 = stilde - inj
        # hoft = (stilde2 / psd ** 0.5).to_timeseries()
        #
        # zoom = hoft.time_slice(merger.time - .3, merger.time + .3)
        # times, freqs, power = zoom.qtransform(.001, logfsteps=100, frange=(20, 512), qrange=(4, 8))

        pylab.subplot(3, 2, (3 * 2) - i)
        # pylab.pcolormesh(times, freqs, power, vmin=0, vmax=50)
        pylab.plot(strain[8192:12288].sample_times, strain[8192:12288], label="Data")
        # pylab.ylim(20, 512)
        pylab.title('Noise of %s - %s' % (event, ifo))
        # pylab.xlabel('Time (s)')
        # pylab.ylabel('Frequency (Hz)')
        # pylab.xlim(times.min(), times.max())
        # pylab.yscale('log')
        # sliding_data = np.array(list(Catalog.sliding_window(white_data, int((window * fs)))))
        # archive.create_dataset(ifo, data=sliding_data)
        # print len(np.array(strain.time_slice(time - .1, time + .1)))
        # print strain.time_slice(time - .1, time + .1)
        # archive.create_dataset("ruido", strain.time_slice(time - 5, time - 4.9))
        # archive.create_dataset("filter"+ifo, white_data.time_slice(time - .1, time + .1))
        # archive.create_dataset("wave"+ifo, (100,))
        # archive.create_dataset("filter"+ifo, (100,))

    # archive.create_dataset("onda sem filtro", data=waves_no_filter)
    # archive.create_dataset("onda com filtro", data=waves_filter)
    # archive.create_dataset("ruido sem filtro", data=noise_no_filter)

    # print "archive " + archive.filename + " successfully generated."
    print "archive " + event + "_data.csv successfully generated."
    # archive.close()
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
