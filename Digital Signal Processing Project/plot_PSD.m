clear all
clc

%number of interp%
nu=10;

%load parame%
load ('lnmT_hnmT.mat');


%period%
T=[0.1:0.1:0.9 1:2:9 10 25 50 75 100];


%this matix created for save all psd and will remove in the end%
totalPSD=interp(ones(1,length(T)),nu);

%my interesting frequency%
f=1./T;

%read sac file%
[t,a,p]=readsacfile('GHM_trilium_Z_50sps.sac');

%remove trend%
a=detrend(a,'constant');

%Definition response%
resp.name='tirll40';
resp.pol=[-0.1103+0.1110i;-0.1103-0.1110i;-86.3;-241.0+178.0i;-241.0-178.0i;-535.0+719.0i;-535.0-719.0i];
resp.zer=[0;0;-68.8;-323;-2530];
resp.const=6.6240e+13;

%calculate PSD%

for n=1:0.5:2
    
     %select segment%
    
    %if n==0;
     %   a1=a(1:180000);
    %else
        a1=a(n*180000:(n+1)*180000);
    %end
    
    %remove instrument response on data%
    data_removed = addremin(resp,a1',50,-1);



    %velocity to acceleration%
    d=diff(data_removed)*50;

    %pwelch%
    [PSD,f]=pwelch(d,10000,9000,f,50);
 

    PSD1=interp(PSD,nu);
    totalPSD=cat(1,totalPSD,PSD1);

    %plot%
     semilogx(T,(10*log10(PSD)),'g')
     hold on
end

%plot hnm & lnm%
 semilogx(hnmT(:,1),hnmT(:,2),'r','linewidth',4);
 hold on
 semilogx(lnmT(:,1),lnmT(:,2),'b','linewidth',4);
 hold on


totalPSD(1,:)=[];
TL=log10(interp(T,nu));

LPSD=10*log10(totalPSD);
LPSD=-abs(LPSD);
