data = edfread("chb15_06.edf");
channel_name = data.SignalLabel21_F8_T8;    % change channel
yaxis = channel_name.';
t=0:1:3600-1;
plot(t,yaxis)







% ictal = 272 -> 392

% 20 - 70 and spike < 100
% a = 0;
% p = 0;
% n = 1;
% while p < 5
%     for i = (5*p)+1:(5*n)
%         seg = channel_name{i,1};    % {raw,column}
%         a = cat(1,a,seg);
%         p = p+1;
%         n = n+1;
%     end
% end
% b = a(2:end,1);
% plot(b)
% xlabel("samples")
% yline(100,'--.m')
% ylabel("amplitude (uV)")