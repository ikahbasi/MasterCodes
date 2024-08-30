%load parame%
load ('lnmT_hnmT.mat');

%%%%%%%%%%%%%%%%
%[TT,LPSD]=n_smooth_octave(LPSD,.02,50)
%%%%%%%%%%%%%%%

%defind end number point of time sequence%
 maxz=length(LPSD(1,:));
 
 %rang of interval PSD for calculate PDF%
 ivl=5;
 
 %select cloum in each time for PDF in this time%
for z=1:maxz
    %equal each selected cloum in each step to r%
    r=LPSD(:,z);
    %Review the subset intervals PSD %
        for k=-200:ivl:-110
            %take average PSD in the interval for plot PDF%
            psd=(2*k+ivl)/2;
            %Getting the number of PSD between two point k & k+ivl%
            q=numel(find(k<r & r<(k+ivl)));
            %Comparison%
                if q==1 || q==2 || q==3
                    %stem average PSD(psd) versus T in logaritmic scale%
                    stem(TL(z),psd,'g','filled','linestyle','none')
                    hold on
                end
        end
end


for z=1:maxz
r=LPSD(:,z);
    for k=-200:ivl:-110
        psd=(2*k+ivl)/2;
        q=numel(find(k<r & r<(k+ivl)));
            if  q==4 || q==5 || q==6
                stem(TL(z),psd,'b','filled','linestyle','none')
                hold on
            end
    end
end

for z=1:maxz
r=LPSD(:,z);
    for k=-200:ivl:-110
        psd=(2*k+ivl)/2;
        q=numel(find(k<r & r<(k+ivl)));
            if q>=7
                stem(TL(z),psd,'r','filled','linestyle','none')
                hold on
            end
    end
end

plot(log10(hnmT(:,1)),hnmT(:,2),'r','linewidth',4);
hold on
plot(log10(lnmT(:,1)),lnmT(:,2),'b','linewidth',4);
hold on