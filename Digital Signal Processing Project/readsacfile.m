function [t,a,p]=readsacfile(sacfile) 
 sacfid=fopen(sacfile,'r'); 
 fparam=zeros(1,70);  iparam=zeros(1,35);  p=zeros(1,40); 
 % Read Parameters 
  fparam=fread(sacfid,70,'float32'); 
  iparam=fread(sacfid,35,'int32'); 
  p=assignparam(fparam,iparam); 
 for j=1:40, if p(j)==-12345 p(j)=nan; end, end; 
 % Read data 
  npts=p(35); a=zeros(1,npts); t=zeros(1,npts); 
  t=p(4):p(1):p(4)+(npts-1)*p(1); 
  fseek(sacfid,158*4,-1);  %(used to be 154?) 
  a(1:npts)=fread(sacfid,npts,'float32'); 
 if isNAN(p(4)) || isNAN(p(1)), 
  t(1:npts)=fread(sacfid,npts,'float32'); 
 end 
 fclose(sacfid); 
 return 
