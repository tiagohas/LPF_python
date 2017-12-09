from __future__ import print_function, division, unicode_literals
 
import wave
import numpy as np
import matplotlib.pyplot as plt
 
def plotar(left, lf):
    plt.figure(1)
    a = plt.subplot(211)
    r = 2 ** 16 / 2
    a.set_ylim([-r, r])
    a.set_xlabel('time [s]')
    a.set_ylabel('sample value [-]')
    x = np.arange(44100) / 44100
    plt.plot(x, left)
    b = plt.subplot(212)
    b.set_xscale('log')
    b.set_xlabel('frequency [Hz]')
    b.set_ylabel('|amplitude|')
    plt.plot(abs(lf))
    plt.savefig('sample-graph.png')
 
 
# abre o arquivo
wr = wave.open('Daft_Punk_Get_Lucky.wav', 'r')
#retorna uma tupla - tupla é um vetor imutavel
par = list(wr.getparams())
par[3] = 0 # The number of samples will be set by writeframes.
 
#cria o arquivo filtrado
ww = wave.open('filtered.wav', 'w')
ww.setparams(tuple(par)) # Use the same parameters as the input file.
 
# cutoff value
cutoff = 1000
 
#lê framerate do arquivo de origem
sz = wr.getframerate()
 
#arquivo inteiro
c = int(wr.getnframes()/sz)
 
#for vai correr o arquivo inteiro range(c)
#e converter apenas para um amostra por segundo
for num in range(c):
    #mostra os processos por vez
    print('Processing {}/{} s'.format(num+1, c))
    '''
       :returns readframes(sz) - le e retorna "n" frames em strings de bytes
       :returns fromstring - transforma em string o byte
       :param dtype=np.int16 - vai sair uma string de 16bits
       da - é um vetor de string
   '''
    da = np.fromstring(wr.readframes(sz), dtype=np.int16)
 
    #da[0::2] retorna o primeiro valor, o ultimo e passo
    #canal da esquerda e direita
    left, right = da[0::2], da[1::2]
    #calculando a simetria do canal esquerdo e direito
    lf, rf = np.fft.rfft(left), np.fft.rfft(right)
    '''
       lf[:lowpass] ele seta 0 até o corte minimo lowpass = 61
   '''
    #lf[:lowpass], rf[:lowpass] = 0, 0
    #linha do ruido
    #lf[55:66], rf[55:66] = 0, 0
    #filtro passa alta
    lf[cutoff:], rf[cutoff:] = 0,0
    #inverso da transformada
    nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
    '''
   pega os inversos e transforma num vetor do tipo int16.
   ele tranforma num vetor 2-D de coluna pelo qual a ultima linha combina os canais esquerdos e
   direitos intercalando com a função ravel() e depois converte em inteiros de 16bits
   '''
    ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
    #ele escreve no arquivo as frequencias filtradas
    ww.writeframes(ns.tostring())
    plotar(left, lf)
 
 
# fecha os dois arquivos o original e o filtrado
wr.close()
ww.close()