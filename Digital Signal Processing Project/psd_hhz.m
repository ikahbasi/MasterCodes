clc;clear all;close all;format;
addpath('/home/hp/practice/func');
% cd('/home/hp/Desktop/football/PSD_30MIN'); 
path=pwd;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
NN=[]; TT=[];
%%%%%%----------------------
data=dir('TDMMO.TD..2018.176.HHZ.SAC');
for j=1:length(data) ; 
    data_j=data(j).name;
    rec= readsac(data_j);
    Seis=rec.trace;
    N=rec.npts;      NN=[NN;N];
    Tsample=rec.tau; TT=[TT;Tsample];
    maxT=(N-1)*Tsample;
    Time=0:Tsample:maxT;
end
NN_Eq=unique(NN,'rows');
TT_Eq=unique(TT,'rows');

%%%%%%%%%%%%%%%%%%%%%%%%%%%
x=dtrend(Seis);
npts=max(size(x));
NFFT = 2^nextpow2(npts);           % Next power of 2 from length of data,
fft_data=fft(x,NFFT);      
amp=abs(fft_data(1:NFFT/2));    
Nfreq=1.0/(2*TT);
freq = Nfreq*linspace(0,1,NFFT/2);
%%%%%%%%%%%%%%%%%%%%%%%%PSD

[pxx,F] = pwelch(x,hanning(NN),[],NN,NFFT);
pxx=pxx*NFFT/2;
%%%%%%%%%%%%%%%%%%%%%%%%%%plot
figure (1);
subplot(2,1,1);
plot (x,'r'),axis tight,grid on,
ax=gca;
ax.XTick = [0:30000:180000+30000];
Cell{1} = {'20:00','20:05','20:10','20:15','20:20','20:25','20:30'};
ax.XTickLabel=Cell{1};
xlabel('Time(min)');ylabel('Amp');title('HHZ');
subplot(2,1,2);
spectrogram(F,10*log10(pxx)),
xlabel('Frequency(Hz)');
ylabel('PSD[10*log(m^2/s^4)/Hz]db');