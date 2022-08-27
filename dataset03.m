data = edfread("chb01_03.edf");
channel_name = data.SignalLabel1_FP1_F7;    % change channel
% pre-ictal = 595 -> 2995
% ictal = 2996 -> 3036
% interictal = 0 -> 594 and 3037 -> 3600
seg = 0;
start = 0;
stop = 1;
p_spike = [];
n_spike = [];
count = 0;
for i = 1000:1004
    seg_divide = channel_name{i,1};    % {raw,column}
    seg = cat(1,seg,seg_divide);
    start = start+1;
    stop = stop+1;
end

for k = 1:1281
    if seg(k) < 100
       seg(k) = 0;
    else
        p_spike = cat(1,p_spike,k);
    end
end
p_spike = cat(1,p_spike,1);

for j = 1:length(p_spike)-1
    if p_spike(j)-p_spike(j+1) == -1
        count = count+1;
    else
        n_spike = cat(1,n_spike,count);
        count = 0;
    end
end
n_spike = n_spike +1;
period = (n_spike / 256)*1000;

for n = 1:length(n_spike)
    if period(n) < 20 | period(n) > 70
        n_spike(n) = [];
    end
end

num_sp = numel(n_spike);

real_seg = seg(2:end,1);
bar(real_seg)
xlabel("samples")
yline(100,'--.m')
ylabel("amplitude (uV)")