clc 
clear all 
close all 

hFig = figure;
x      = 0;   % Screen position
y      = 0;   % Screen position
width  = 1100; % Width of figure
height = 720;
set(hFig, 'Position', [x y width height])

subplot (2,2,1)
fname1=fopen('../Host_10/HD_10.txt', 'r');
val=textscan(fname1,'%d %f', 'HeaderLines',1);
fclose(fname1);
Packet_num1=val{1};
latency1=val{2}/1000;
bin_log_scale=calculate_histogram_bins(latency1,20,1);
histogram(latency1, bin_log_scale, 'FaceColor','blue','EdgeColor','k', 'LineWidth' ,0.2)
xlabel(['Packet latency (ms)', newline,'\bf (a)'],'FontSize', 15,'FontName','Times New Roman')
ylabel ( 'Frequency','FontSize' , 15,'FontName','Times New Roman')

a = get(gca,'XLabel');
b = get(gca,'YLabel');
set(gca,'YLabel',b,'FontName','Times','fontsize',12)
set(gca,'XLabel',a,'FontName','Times','fontsize',12)

ax = gca;
ax.YAxis.Exponent = 0;
xlim([0, 10])
ylim([0, 10])
xticks('auto');
% yticks([0,2,4,6,8,10]);



subplot (2,2,2)
fname2=fopen('../Host_10/HD_100.txt', 'r');
val=textscan(fname2,'%d %f', 'HeaderLines',1);
fclose(fname2);
Packet_num2=val{1};
latency2=val{2}/1000;
bin_log_scale=calculate_histogram_bins(latency2,20,1);
histogram(latency2, bin_log_scale, 'FaceColor','m','EdgeColor','k', 'LineWidth' ,0.2)
xlabel(['Packet latency (ms)', newline,'\bf (b)'],'FontSize', 15,'FontName','Times New Roman')
ylabel ( 'Frequency','FontSize' , 15,'FontName','Times New Roman')

a = get(gca,'XLabel');
b = get(gca,'YLabel');
set(gca,'YLabel',b,'FontName','Times','fontsize',12)
set(gca,'XLabel',a,'FontName','Times','fontsize',12)

% ax = gca;
% ax.YAxis.Exponent = 1;
xlim([0, 10])
ylim([0, 100])
xticks('auto');
% yticks([0,5, 10, 15, 20]);


h=subplot (2,2,3);
fname3=fopen('../Host_10/HD_1000.txt', 'r');
val=textscan(fname3,'%d %f', 'HeaderLines',1);
fclose(fname3);
Packet_num3=val{1};
latency3=val{2}/1000;
bin_log_scale=calculate_histogram_bins(latency3,20,1);
histogram(latency3, bin_log_scale, 'FaceColor','r','EdgeColor','k', 'LineWidth' ,0.2)
xlabel(['Packet latency (ms)', newline,'\bf (c)'],'FontSize', 15,'FontName','Times New Roman')
ylabel ( 'Frequency','FontSize' , 15,'FontName','Times New Roman')

a = get(gca,'XLabel');
b = get(gca,'YLabel');
set(gca,'YLabel',b,'FontName','Times','fontsize',12)
set(gca,'XLabel',a,'FontName','Times','fontsize',12)

% ax = gca;
% ax.YAxis.Exponent = 2;
xlim([0, 10])
ylim([0, 1000])
xticks('auto');
% yticks([0,5, 10]);

% Align the third subplot to the middle of the row
pos = get(h, 'position');
pos(1) = 0.35; % Adjust the horizontal position to align to the middle
set(h, 'position', pos);


set(hFig,'PaperSize',[10 7.5]);
print(hFig,'NoML_Histogram_H10','-dpdf') % then print it
% print(hFig,'HD_Histogram','-dtiff') % then print it


function bin_log_scale=calculate_histogram_bins(packet_data, n_bins, min_latency_ms)
    max_latency_ms = max(packet_data);
    bin_log_scale = logspace(log10(min_latency_ms), log10(max_latency_ms), n_bins);
end