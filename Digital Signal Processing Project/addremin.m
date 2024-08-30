function timeout = addremin(resp,timein,sps,cont)
%-----------------------------------------------------------------------
%[timeout]=addremin(resp,timein,sps,cont);
%
%ADDREMIN is to add or remove the instrument respeonse to relavent data
%
%Input:
% resp - the instrument response matrice. The first line contains
%        amplitude and sensitivity,and the second line contains
%        the number of zeros(first column) and the number of the
%        poles(second column).And then the next lines are for 
%        the real parts(first column) and the image parts(second
%        column) of the zeros, followed by those of poles (rad). 
% timein - the iuput time series as a column vector;
%  sps - the sampling frequency;
%  cont - the control, -1 for removing, and +1 for adding
%
%  Xu Lisheng, 1997-04-14
%  Hamburg University, Hamburg, Germany
%----------------------------------------------------------------------

%Make the length of the timein be the power of 2
% % timein = timein(:); % Make the timein a column series
% % timein = detrend(timein);%Remove the mean and the trend
len = 2.^nextpow2(length(timein));

%Create a frequency vector
fvec = sps * linspace(0,1,len)';

%Change to the angle frequency
omeg = zeros(size(fvec)) + 1i * 2 * pi * fvec;

%Pick out the poles and the zeros and the amplitude
% % amp = resp(1,1) * resp(1,2);    % Amplitude
% % nzero = resp(2,1);
% % npole = resp(2,2);
% % zerores = (resp(3:2+nzero,1) + i * resp(3:2+nzero,2)) * 2 * pi;
% % poleres = (resp(3+nzero:2+nzero+npole,1) + i * resp(3+nzero:2+nzero+npole,2)) * 2 * pi;
amp = resp.const;
zerores = resp.zer;
poleres = resp.pol;
 
%Calculate the zeros-response for different frequency
tem1=zeros(len,length(zerores));
for k = 1:length(zerores)
    tem0 = real(zerores(k)) * ones(len,1) + 1i * imag(zerores(k)) * ones(len,1);
    tem1(:,k) = omeg - tem0;
end
%tem1 = tem1';
zinst = prod(tem1,2);
 
clear tem1 tem0

%Calculate the poles-response for different frequency
tem1=zeros(len,length(poleres));
for k = 1:length(poleres)
    tem0 = real(poleres(k)) * ones(len,1) + 1i * imag(poleres(k)) * ones(len,1);
    tem1(:,k) = omeg - tem0;
end
%tem1 = tem1';
pinst = prod(tem1,2);

clear tem1 tem0

%zeros and poles response are put together

norm2in = abs(pinst) .^ 2;
maxv = max(max(norm2in));

%Determine the waterlevel according to the specific case
temp = norm2in;
whozero = find(temp == 0);
temp(whozero) = maxv * ones(size(whozero));
minv = min(min(temp));
norm2in(whozero) = minv * ones(size(whozero));

instres = amp * (zinst .* conj(pinst)) ./ norm2in;

clear norm2in
 
%figure,loglog(fvec,abs(instres));

%Work with data
if cont == 1 % Add the instrument response
   fftdat = fft(timein,len);
   fftime = fftdat .* instres;
elseif cont == -1 % Remove the instrument response
   fftdat = fft(timein,len);
   norm2in = abs(instres).^2;
   maxv = max(max(norm2in));

   %Determine the waterlevel according to the specific case
   temp = norm2in;
   whozero = find(temp == 0);
   temp(whozero) = maxv * ones(size(whozero));
   minv = min(min(temp));
   norm2in(whozero) = minv .* ones(size(whozero));
 
   fftime = (fftdat .* conj(instres)) ./ norm2in;
end
 
clear norm2in fftdat

% Return to the time domain
timeout = real(ifft(fftime));

%Original length of the time series is recovered
timeout = timeout(1:length(timein));
%timeout=btfil(2*sps/5.,0.01,timeout,sps);%filtering
%timeout=detrend(timeout,0);%Delete the trend

%Display the comparison of the input and output
%figure,plot(timeout,'r');
%title('Output Data');
%figure,plot(timein,'g');
%title('Input Data')
%=========end=============================================================
