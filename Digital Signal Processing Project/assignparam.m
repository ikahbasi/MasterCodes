 function p=assignparam(fparam,iparam) 
 p=zeros(1,40); 
 p(1:3)=fparam(1:3);            %delta,depmin,depmax, 
 p(4:5)=fparam(6:7);            %B,E 
 p(6)=fparam(8);                %Event Origin Time 
 p(7:16)=fparam(11:20);         %T0 - T9 
 p(17:24)=fparam(32:39);        %STLA,LO,EL,DP,EVLA,LO,EL,DP 
 p(25:28)=fparam(51:54);        %Dist,Az,BAz,GCArc 
 p(29:34)=iparam(1:6);          %Year,Day,Hour,Min,Sec,MillSec 
 p(35)=iparam(10);              %Npts 
 p(36:38)=iparam(16:18);        %IFType,IDep,IZType 
 p(39:40)=[iparam(23) iparam(25)];   %IevTyp,ISynth 
 return 
